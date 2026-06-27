

.PHONY: version up-major up-minor up-patch print-version serve-docs clean-docs

version:
	@uv version #| awk '{print $2}'

up-major:  # Upgrading X in X.Y.Z
	@echo "Upgrading major tag from version"
	@uv version --bump=major
	$(MAKE) print-version

up-minor:  # Upgrading Y in X.Y.Z
	@echo "Upgrading minor tag from version"
	@uv version --bump=minor
	$(MAKE) print-version

up-patch:  # Upgrading Z in X.Y.Z
	@echo "Upgrading patch tag from version"
	@uv version --bump=patch
	$(MAKE) print-version

print-version:
	@echo "Printing version to .project-version"
	@uv version | awk '{print $$2}' > .project-version


# ---------------------

serve-docs:
	@export DISABLE_MKDOCS_2_WARNING=true
	@mkdocs serve -o --livereload

clean-docs:
	@echo "Cleaning built docs..."
	@rm -rf site/

build-docs:
	@mkdocs build

# ---------------------

clean-dist:
	@rm -rf dist/
