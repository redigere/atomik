.PHONY: all lint check test install-deps apply-core clean help
.PHONY: apply-only-repos apply-only-packages apply-only-security apply-only-desktop
.PHONY: apply-extra apply-extra-kde apply-extra-gnome apply-extra-flatpak apply-extra-codium apply-extra-devtools

PROJECT_DIR := $(shell pwd)
ANSIBLE_PLAYBOOK = ansible-playbook $(PROJECT_DIR)/ansible/site.yml -i $(PROJECT_DIR)/ansible/inventories/localhost/hosts.yml
E2E_PLAYBOOK = ansible-playbook $(PROJECT_DIR)/tests/e2e.yml -i $(PROJECT_DIR)/ansible/inventories/localhost/hosts.yml -c local
all: lint test

help:
	@echo "Usage:"
	@echo "  make all                  Run lint + test"
	@echo "  make lint                 Syntax check all playbooks"
	@echo "  make test                 Run e2e tests"
	@echo "  make apply-core           Apply full configuration"
	@echo "  make apply-only-repos     Apply repos only"
	@echo "  make apply-only-packages  Apply packages only"
	@echo "  make apply-only-security  Apply security only"
	@echo "  make apply-only-desktop   Apply desktop only"
	@echo "  make apply-extra          Apply all extra configs"
	@echo "  make apply-extra-kde      Apply KDE panels/theme"
	@echo "  make apply-extra-gnome    Apply GNOME theme/settings"
	@echo "  make apply-extra-flatpak  Install non-system Flatpak apps"
	@echo "  make apply-extra-codium   Install and configure debloated VSCodium"
	@echo "  make apply-extra-devtools Install dev tools (nvm, pnpm, rustup, sdkman, opencode)"
	@echo "  make install-deps         Install ansible-core + collections"
	@echo "  make clean                Remove ansible retry files"

apply-extra: apply-extra-kde apply-extra-gnome apply-extra-devtools

apply-extra-kde:
	python3 extra/kde/apply_kde.py

apply-extra-gnome:
	python3 extra/gnome/apply_gnome.py

apply-extra-flatpak:
	python3 extra/flatpak/apply_flatpak.py

apply-extra-codium:
	python3 extra/codium/apply_codium.py

apply-extra-devtools:
	python3 extra/devtools/apply_devtools.py

lint:
	cd ansible && ansible-playbook --syntax-check site.yml
	cd ansible && ansible-playbook --syntax-check ../tests/e2e.yml
	cd ansible && ansible-playbook --syntax-check ../extra/flatpak/site.yml
	cd ansible && ansible-playbook --syntax-check ../extra/codium/site.yml

test:
	$(E2E_PLAYBOOK)

install-deps:
	pkexec rpm-ostree install -y --idempotent --apply-live ansible-core python3-ansible-lint
	pkexec ansible-galaxy collection install ansible.posix community.general

apply-only-repos:
	pkexec $(ANSIBLE_PLAYBOOK) --tags repos

apply-only-packages:
	pkexec $(ANSIBLE_PLAYBOOK) --tags packages

apply-only-security:
	pkexec $(ANSIBLE_PLAYBOOK) --tags security

apply-only-desktop:
	pkexec $(ANSIBLE_PLAYBOOK) --tags desktop

apply-core:
	pkexec $(ANSIBLE_PLAYBOOK)

clean:
	rm -f ansible/*.retry tests/*.retry
