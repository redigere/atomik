.PHONY: all lint check test install-deps apply clean help
.PHONY: apply-repos apply-packages apply-security apply-desktop apply-devtools

ANSIBLE_PLAYBOOK = ansible-playbook ansible/site.yml -i ansible/inventories/localhost/hosts.yml
E2E_PLAYBOOK = ansible-playbook tests/e2e.yml -i ansible/inventories/localhost/hosts.yml -c local
ROLES = repos packages security desktop devtools

all: lint test

help:
	@echo "Usage:"
	@echo "  make all              Run lint + test"
	@echo "  make lint             Syntax check all playbooks"
	@echo "  make test             Run e2e tests"
	@echo "  make apply            Apply full configuration"
	@echo "  make apply-<role>     Apply single role ($(ROLES))"
	@echo "  make install-deps     Install ansible-core + collections"
	@echo "  make clean            Remove ansible retry files"

lint:
	cd ansible && ansible-playbook --syntax-check site.yml
	cd ansible && ansible-playbook --syntax-check ../tests/e2e.yml

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

apply-devtools:
	pkexec $(ANSIBLE_PLAYBOOK) --tags devtools

clean:
	rm -f ansible/*.retry tests/*.retry
