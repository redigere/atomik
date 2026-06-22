# Atomik

Atomik is a declarative configuration runtime applied to existing Fedora atomic installations. It adapts to the detected desktop environment at runtime and never generates ISO images.

## Requirements

Four gigabytes of RAM minimum. The system must already be running Fedora Silverblue, Kinoite, or Cosmic Atomic.

## How It Works

The CLI applies configuration in a variant specific sequential pipeline. Repositories are configured first, then packages are installed, security hardening is applied, desktop settings are configured, extensions are deployed, and container environments are set up last. Every step is idempotent and can be safely re executed.

The pipeline handles the rpm-ostree reboot lifecycle automatically. After packages are staged, the system applies changes to the live filesystem so subsequent steps can execute immediately without requiring a manual reboot mid pipeline.

## Security

Firewalld, audit rules, fail2ban, and hardened kernel parameters are applied by default. SSH is restricted to key only authentication. Process limits, file descriptor limits, and memory locking limits are raised to support heavy concurrent workloads.

## Memory Management

The kernel is tuned for desktop interactivity rather than server throughput. ZRAM provides compressed RAM based swap. Systemd oomd monitors cgroup memory pressure and terminates offending processes when thresholds are exceeded. The oomd daemon is the single process killer and runs with generous thresholds tuned for desktop workloads.

## Configuration

All configuration lives in YAML files under the config directory. Rust source code contains only execution logic. Shell commands are declared as strings in YAML and interpolated at runtime with named arguments. A schema validation layer checks every configuration file at load time.

## Reset

A recovery utility completely reverts the system to a clean baseline. It resets desktop settings, uninstalls custom packages, removes third party repositories, deletes installed fonts and wallpapers, and refreshes the system font cache.

## Development

The codebase is written in Rust. Each module handles exactly one domain. The CI pipeline runs formatting checks, linting with warnings treated as errors, the full test suite, and a signoff verification step. No third party GitHub Actions are used.
