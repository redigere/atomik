.PHONY: all lint check test test-e2e apply apply-single install-deps

ANSIBLE_PLAYBOOK = ansible-playbook ansible/site.yml -i ansible/inventories/localhost/hosts.yml
E2E_PLAYBOOK = ansible-playbook tests/e2e.yml -i ansible/inventories/localhost/hosts.yml -c local

all: lint check test

lint:
	cd ansible && ansible-playbook --syntax-check site.yml

check:
	cd ansible && ansible-playbook --check site.yml

test:
	$(E2E_PLAYBOOK)

install-deps:
	pkexec rpm-ostree install -y --idempotent --apply-live ansible-core python3-ansible-lint
	pkexec ansible-galaxy collection install ansible.posix community.general

apply:
	pkexec $(ANSIBLE_PLAYBOOK)

apply-single:
	pkexec $(ANSIBLE_PLAYBOOK) --tags $(TAG)
