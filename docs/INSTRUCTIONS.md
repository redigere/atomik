# Atomik Agentic Management Guidelines

This document serves as the primary technical directive for all AI agents and automated tools managing the Atomik codebase. It establishes the uncompromising standards for code quality, system integrity, and architectural consistency.

## Core Directives

The first directive is the absolute preservation of system integrity. Under no circumstances shall an agent introduce code that is vulnerable, experimental, or poorly defined. All implementations must be final, robust, and idiomatic. Placeholders, comments in source files, and fallback mechanisms are strictly forbidden. If an operation cannot be performed exactly as specified, the agent must report a fatal failure rather than attempting a workaround.

The second directive is the strict separation of data and logic. All configuration parameters, shell commands, and system settings must reside within the YAML configuration files. Rust and Python source code must function exclusively as execution engines for this declarative data. Agents must never hardcode strings, paths, or commands directly into the source logic.

## Container Orchestration Standards

The container management subsystem is designed for infinite recursive nesting. This is achieved by mounting the host's Podman and Storage configurations into the containerized environment. Any modification to the container tasks must ensure that `/dev/fuse`, `/etc/containers/containers.conf`, and `/etc/containers/storage-nested.conf` are correctly propagated down the chain.

The startup hooks located in `/etc/profile.d/z-atomik-container-hook.sh` must remain distro-agnostic but highly specialized for Arch and Fedora. These hooks are the primary mechanism for first-boot initialization within Distrobox environments. Agents must verify that any new hook logic is idempotent and does not introduce latency to standard shell startup.

## Status Tracking and Auditability

Atomik maintains a complete execution history in `/etc/atomik-status.json`. This file must be updated after every successful configuration apply operation. The structure must remain a flat JSON array of objects, where each object contains an ISO-8601 timestamp, the list of executed steps, and the final status. Agents must ensure this file is never corrupted and remains the single source of truth for the system's applied state.

## Technical Quality and Safety

All code must be verified through the project's test suite and linted against the strictest standards. Agents are responsible for the entire lifecycle: from empirical reproduction of requirements to exhaustive validation. A task is considered complete only when the behavioral correctness is confirmed and the structural integrity is verified within the full project context. No regression is acceptable. Every change must be surgical, intentional, and perfectly aligned with the macOS-on-Linux vision established in the ARCHITECTURE documentation.
