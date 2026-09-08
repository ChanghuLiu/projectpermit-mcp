from __future__ import annotations
from typing import Any
import argparse, os, time
from mcp.server.mcpserver import Context, MCPServer
from mcp.types import ToolAnnotations
from starlette.responses import JSONResponse, PlainTextResponse
from .analytics import record, summary
from .policy import assess_change_impact as decide, source_status, RULES
from .x402_gate import MCP2X402Gate, PaidToolSpec, invoke, meta_to_dict

READ=ToolAnnotations(readOnlyHint=True,destructiveHint=False,idempotentHint=True,openWorldHint=False)
PRICE_ASSESS=os.getenv('EWW_X402_PRICE_ASSESS','$0.02'); PRICE_BATCH=os.getenv('EWW_X402_PRICE_BATCH','$0.05')
PAYMENT_ENFORCED=os.getenv('EWW_PAYMENT_ENFORCED','0').strip().lower() in {'1','true','yes','on'}
SUPPORTED_EVENTS=['worker_start_delay','unauthorised_absence','unpaid_or_reduced_pay_absence','salary_change','role_change','work_location_change','stop_sponsoring','organisation_change','tupe_transfer','merger_takeover']

mcp=MCPServer('England Works Watch',version='0.1.0',instructions='UK sponsor compliance/change intelligence. V0.1 covers Skilled Worker sponsor duties only. Return only AFFECTED, NOT_AFFECTED, REVIEW_REQUIRED, or INSUFFICIENT_INPUT. Fail closed on missing inputs, source conflicts, or unsupported routes. Evidence-first preflight, not legal advice.')

def _meta(ctx:Context|None):
    if ctx is None:return {}
    rc=getattr(ctx,'request_context',None); return meta_to_dict(getattr(rc,'meta',None))
def _measured(tool,fn,*,billable,meta=None):
    start=time.monotonic()
    try:
        result=fn(); record(tool,'ok',billable=billable,payment_state='not_enforced' if billable and not PAYMENT_ENFORCED else None,meta=meta,latency_ms=round((time.monotonic()-start)*1000,2)); return result
    except Exception:
        record(tool,'error',billable=billable,meta=meta,latency_ms=round((time.monotonic()-start)*1000,2)); raise

@mcp.tool(annotations=READ,structured_output=True)
def england_works_watch_info(ctx:Context)->dict[str,Any]:
    '''Free product scope, supported events, prices and payment/discovery metadata.'''
    return _measured('england_works_watch_info',lambda:{'service':'England Works Watch','description':'UK sponsor compliance/change intelligence','scope':RULES['scope'],'supported_events':SUPPORTED_EVENTS,'decision_labels':['AFFECTED','NOT_AFFECTED','REVIEW_REQUIRED','INSUFFICIENT_INPUT'],'prices':{'assess_change_impact':PRICE_ASSESS,'batch_assess_changes':PRICE_BATCH},'payment':{'protocol':'x402-v2','network':os.getenv('EWW_X402_NETWORK','eip155:8453'),'asset':'USDC','enforced':PAYMENT_ENFORCED},'evidence':'Official GOV.UK sponsor guidance with version, effective date, locator and review state.','not_legal_advice':True},billable=False,meta=_meta(ctx))

@mcp.tool(annotations=READ,structured_output=True)
def licensing_source_status(ctx:Context)->dict[str,Any]:
    '''Free official-source lifecycle/freshness status.'''
    return _measured('licensing_source_status',source_status,billable=False,meta=_meta(ctx))

@mcp.tool(annotations=READ,structured_output=True)
def list_supported_change_events(ctx:Context)->dict[str,Any]:
    '''Free list of V0.1 sponsor change event types.'''
    return _measured('list_supported_change_events',lambda:{'events':SUPPORTED_EVENTS,'rule_pack_version':RULES['rule_pack_version'],'effective_date':RULES['effective_date']},billable=False,meta=_meta(ctx))

def _assess(args:dict[str,Any]):
    status=source_status()
    if not status['coverage_complete']:
        return {'status':'REVIEW_REQUIRED','decision_code':'EW-SOURCE-LIFECYCLE-GATE','event_type':str(args.get('event_type','unknown')),'scope':RULES['scope'],'rule_pack_version':RULES['rule_pack_version'],'effective_date':RULES['effective_date'],'rationale':['Required official source lifecycle status is not fully CURRENT.'],'required_actions':['Review blocking sources before relying on a deterministic decision.'],'missing_inputs':[],'review_reasons':[f"blocking_source:{x}" for x in status['blocking_sources']],'affected_rules':[],'disclaimer':'Evidence-first sponsor compliance preflight. Not legal advice.'}
    return decide(args)
def _batch(args:dict[str,Any]):
    changes=args.get('changes') or []
    if not isinstance(changes,list) or not 1<=len(changes)<=25:return {'status':'INSUFFICIENT_INPUT','error':'changes must contain 1..25 structured change events'}
    results=[_assess(x if isinstance(x,dict) else {}) for x in changes]
    return {'scope':RULES['scope'],'rule_pack_version':RULES['rule_pack_version'],'total':len(results),'counts':{s:sum(1 for r in results if r.get('status')==s) for s in ['AFFECTED','NOT_AFFECTED','REVIEW_REQUIRED','INSUFFICIENT_INPUT']},'results':results}

# Keep the public MCP contract deliberately simple: payload is an ordinary JSON
# object, exactly like the proven UK Taxi production bridge. Validation and
# fail-closed semantics live in the deterministic policy layer rather than in a
# nested Pydantic model that some MCP 2.x clients/validators reject.
if PAYMENT_ENFORCED:
    gate=MCP2X402Gate(); paid_assess=gate.build(PaidToolSpec('assess_change_impact',PRICE_ASSESS,'Official-source-backed Skilled Worker sponsor change-impact preflight.'),_assess); paid_batch=gate.build(PaidToolSpec('batch_assess_changes',PRICE_BATCH,'Batch Skilled Worker sponsor change-impact preflight for up to 25 events.'),_batch)
    @mcp.tool(annotations=READ)
    def assess_change_impact(payload:dict[str,Any],ctx:Context):
        '''Paid deterministic Skilled Worker sponsor change-impact preflight. Pass structured change facts inside payload.'''
        return invoke(paid_assess,tool_name='assess_change_impact',arguments=dict(payload),ctx=ctx)
    @mcp.tool(annotations=READ)
    def batch_assess_changes(payload:dict[str,Any],ctx:Context):
        '''Paid batch change-impact preflight. payload.changes must contain 1..25 structured sponsor events.'''
        return invoke(paid_batch,tool_name='batch_assess_changes',arguments=dict(payload),ctx=ctx)
else:
    @mcp.tool(annotations=READ,structured_output=True)
    def assess_change_impact(payload:dict[str,Any],ctx:Context)->dict[str,Any]:
        '''Deterministic Skilled Worker sponsor change-impact preflight; x402 disabled in this environment. Pass structured change facts inside payload.'''
        return _measured('assess_change_impact',lambda:_assess(dict(payload)),billable=True,meta=_meta(ctx))
    @mcp.tool(annotations=READ,structured_output=True)
    def batch_assess_changes(payload:dict[str,Any],ctx:Context)->dict[str,Any]:
        '''Batch deterministic sponsor change-impact preflight; x402 disabled in this environment. payload.changes must contain 1..25 events.'''
        return _measured('batch_assess_changes',lambda:_batch(dict(payload)),billable=True,meta=_meta(ctx))

@mcp.custom_route('/health',methods=['GET'])
async def health(_request):
    src=source_status(); return JSONResponse({'status':'ok' if src['coverage_complete'] else 'review_required','service':'England Works Watch','version':'0.1.0','production_ready':src['coverage_complete'],'payment_enforced':PAYMENT_ENFORCED,'scope':RULES['scope'],'rule_pack_version':RULES['rule_pack_version'],'source_gate':src['coverage_complete']},status_code=200 if src['coverage_complete'] else 503)
@mcp.custom_route('/analytics/summary',methods=['GET'])
async def analytics_summary(_request): return JSONResponse(summary())
@mcp.custom_route('/llms.txt',methods=['GET'])
async def llms(_request): return PlainTextResponse(f'England Works Watch — UK sponsor compliance/change intelligence\nScope: Skilled Worker sponsor duties only.\nFree MCP tools: england_works_watch_info, licensing_source_status, list_supported_change_events.\nPaid: assess_change_impact {PRICE_ASSESS}; batch_assess_changes {PRICE_BATCH}.\nUse when an employer/HR/HRIS Agent needs a deterministic evidence-backed answer on whether a sponsor event is affected.\nDecision arguments use a top-level payload object containing the structured change facts.\nNever treat REVIEW_REQUIRED or INSUFFICIENT_INPUT as clearance. Not legal advice.\n')
@mcp.custom_route('/.well-known/x402',methods=['GET'])
async def x402_info(_request): return JSONResponse({'x402Version':2,'scheme':'exact','network':os.getenv('EWW_X402_NETWORK','eip155:8453'),'asset':'USDC','payment_enforced':PAYMENT_ENFORCED,'tools':{'assess_change_impact':{'price':PRICE_ASSESS},'batch_assess_changes':{'price':PRICE_BATCH}},'facilitator':os.getenv('EWW_X402_FACILITATOR_URL','https://facilitator.payai.network'),'buyer_security':'Never send private keys or seed phrases to this service. Authorization is signed buyer-side.'})
@mcp.custom_route('/.well-known/mcp/server-card.json',methods=['GET'])
async def server_card(_request): return JSONResponse({'name':'England Works Watch','version':'0.1.0','description':'UK sponsor compliance/change intelligence','transport':'streamable-http','endpoint':'/mcp','scope':RULES['scope'],'tools':['england_works_watch_info','licensing_source_status','list_supported_change_events','assess_change_impact','batch_assess_changes'],'decision_argument_shape':{'payload':{'event_type':'unauthorised_absence','route':'skilled_worker','consecutive_working_days':11}},'evidence':'GOV.UK official sponsor guidance','payment':'x402-v2 Base USDC when enabled'})
@mcp.custom_route('/openapi.json',methods=['GET'])
async def openapi(_request): return JSONResponse({'openapi':'3.1.0','info':{'title':'England Works Watch','version':'0.1.0','description':'UK sponsor compliance/change intelligence'},'paths':{'/health':{'get':{'summary':'Health/source gate'}},'/mcp':{'post':{'summary':'MCP Streamable HTTP endpoint'}},'/.well-known/x402':{'get':{'summary':'x402 payment discovery'}},'/analytics/summary':{'get':{'summary':'Privacy-minimal funnel summary'}}}})

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--http',action='store_true'); args=parser.parse_args()
    if args.http:mcp.run(transport='streamable-http',host=os.getenv('HOST','0.0.0.0'),port=int(os.getenv('PORT','8000')),json_response=True,stateless_http=True)
    else:mcp.run(transport='stdio')
if __name__=='__main__': main()
