FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
COPY src ./src
COPY data ./data
COPY tests ./tests
COPY scripts ./scripts
RUN pip install --no-cache-dir '.[x402,test]' \
 && pytest -q \
 && PYTHONPATH=src python scripts/acceptance_report.py \
 && PYTHONPATH=src python scripts/audit_sources.py
# Runtime-import gate: the installed package resolves its evidence bundle outside
# site-packages. Bind that expected path to the immutable image evidence bundle,
# then import the installed package (without PYTHONPATH) so this class of startup
# regression fails the build rather than Railway healthcheck.
RUN ln -s /app/data /usr/local/lib/python3.12/data \
 && python -c "from england_works_watch.policy import source_status; s=source_status(); assert s['coverage_complete']; print('installed-runtime-import=PASS', s['rule_pack_version'])"
RUN useradd --uid 10001 --create-home appuser && mkdir -p /data && chown -R appuser:appuser /data /app
USER appuser
ENV HOST=0.0.0.0 PORT=8000 EWW_RUNTIME_DIR=/data
CMD ["england-works-watch", "--http"]
