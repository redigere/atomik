.PHONY: all lint check test install-deps apply clean help
.PHONY: apply-repos apply-packages apply-security apply-desktop apply-extra apply-extra-kde apply-extra-gnome apply-extra-flatpak apply-extra-codium apply-extra-devtools

ANSIBLE_PLAYBOOK = ansible-playbook ansible/site.yml -i ansible/inventories/localhost/hosts.yml
E2E_PLAYBOOK = ansible-playbook tests/e2e.yml -i ansible/inventories/localhost/hosts.yml -c local
ROLES = repos packages security desktop

all: lint test

help:
	@echo "Usage:"
	@echo "  make all              Run lint + test"
	@echo "  make lint             Syntax check all playbooks"
	@echo "  make test             Run e2e tests"
	@echo "  make apply            Apply full configuration"
	@echo "  make apply-<role>     Apply single role ($(ROLES))"
	@echo "  make apply-extra      Apply all extra configs"
	@echo "  make apply-extra-kde  Apply KDE panels/theme"
	@echo "  make apply-extra-gnome Apply GNOME theme/settings"
	@echo "  make apply-extra-flatpak Install non-system Flatpak apps"
	@echo "  make apply-extra-codium  Install and configure debloated VSCodium"
	@echo "  make apply-extra-devtools Install dev tools (nvm, pnpm, rustup, sdkman, opencode)"
	@echo "  make install-deps     Install ansible-core + collections"
	@echo "  make clean            Remove ansible retry files"

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

apply:
	pkexec $(ANSIBLE_PLAYBOOK)

apply-repos:
	pkexec $(ANSIBLE_PLAYBOOK) --tags repos

apply-packages:
	pkexec $(ANSIBLE_PLAYBOOK) --tags packages

apply-security:
	pkexec $(ANSIBLE_PLAYBOOK) --tags security

apply-desktop:
	pkexec $(ANSIBLE_PLAYBOOK) --tags desktop

clean:
	rm -f ansible/*.retry tests/*.retry
