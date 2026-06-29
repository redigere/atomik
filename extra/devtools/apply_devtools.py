#!/usr/bin/env python3
import os
import subprocess
import sys

HOME = os.path.expanduser("~")
BASHRC_D = os.path.join(HOME, ".bashrc.d")
FISH_CONFD = os.path.join(HOME, ".config", "fish", "conf.d")
BASH_D = os.path.join(HOME, ".bash.d")
BASHRC = os.path.join(HOME, ".bashrc")


def run(cmd, check=True):
    print(f"  -> {cmd[:120]}...")
    return subprocess.run(cmd, shell=True, check=check, text=True,
                          capture_output=True)


def mkdir(path):
    os.makedirs(path, exist_ok=True)
    print(f"  -> created {path}")


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"  -> wrote {path}")


def remove(path):
    if os.path.exists(path):
        os.remove(path)
        print(f"  -> removed {path}")


def setup_shell():
    print("[shell] Configuring shell environment")
    mkdir(BASHRC_D)
    mkdir(FISH_CONFD)

    # Migrate old .bash.d
    if os.path.isdir(BASH_D) and not os.path.islink(BASH_D):
        run(f"cp -rP {BASH_D}/* {BASHRC_D}/ || true")
        run(f"rm -rf {BASH_D}")
        print("  -> migrated .bash.d to .bashrc.d")
    if not os.path.islink(BASH_D) and not os.path.exists(BASH_D):
        os.symlink(".bashrc.d", BASH_D)
        print("  -> symlinked .bash.d -> .bashrc.d")

    # JetBrains aliases
    write_file(os.path.join(BASHRC_D, "jetbrains.sh"),
               'if command -v dex >/dev/null 2>&1; then\n'
               '    alias jetbrains-toolbox="dex $HOME/.local/share/applications/jetbrains-toolbox.desktop"\n'
               '    alias idea="dex $HOME/.local/share/applications/jetbrains-idea-2962247c-c234-4f4f-b69a-1ba655f7a676.desktop"\n'
               '    alias android-studio="dex $HOME/.local/share/applications/jetbrains-studio-dc863395-7115-4ff2-948e-3f642bc481dd.desktop"\n'
               'fi\n')

    write_file(os.path.join(FISH_CONFD, "jetbrains.fish"),
               'if command -v dex >/dev/null 2>&1\n'
               '    alias jetbrains-toolbox "dex $HOME/.local/share/applications/jetbrains-toolbox.desktop"\n'
               '    alias idea "dex $HOME/.local/share/applications/jetbrains-idea-2962247c-c234-4f4f-b69a-1ba655f7a676.desktop"\n'
               '    alias android-studio "dex $HOME/.local/share/applications/jetbrains-studio-dc863395-7115-4ff2-948e-3f642bc481dd.desktop"\n'
               'end\n')

    # Remove old ATOMIK BASH.D block from .bashrc
    if os.path.isfile(BASHRC):
        with open(BASHRC) as f:
            content = f.read()
        new_content = []
        skip = False
        for line in content.splitlines(True):
            if "# BEGIN ATOMIK BASH.D" in line:
                skip = True
            elif "# END ATOMIK BASH.D" in line:
                skip = False
                continue
            if not skip:
                new_content.append(line)
        content = "".join(new_content)

        # Add ATOMIK BASHRC.D block if not present
        if "# BEGIN ATOMIK BASHRC.D" not in content:
            block = (
                "# BEGIN ATOMIK BASHRC.D\n"
                'if [ -d ~/.bashrc.d ]; then\n'
                '    for rc in ~/.bashrc.d/*; do\n'
                '        if [ -f "$rc" ]; then\n'
                '            . "$rc"\n'
                '        fi\n'
                '    done\n'
                'fi\n'
                "# END ATOMIK BASHRC.D\n"
            )
            content += "\n" + block
        with open(BASHRC, "w") as f:
            f.write(content)
        print("  -> updated .bashrc")

    # Configure JetBrains terminal
    import glob
    jetbrains_dirs = glob.glob(
        os.path.join(HOME, ".var", "app", "*JetBrains*", "config", "options")
    )
    android_dirs = glob.glob(
        os.path.join(HOME, ".config", "Google", "AndroidStudio*", "options")
    )
    for d in jetbrains_dirs + android_dirs:
        terminal_xml = os.path.join(d, "terminal.xml")
        if not os.path.isfile(terminal_xml):
            write_file(
                terminal_xml,
                '<application>\n'
                '  <component name="TerminalOptionsProvider">\n'
                '    <option name="shellPath" value="flatpak-spawn --host /usr/bin/fish" />\n'
                '  </component>\n'
                '</application>\n',
            )


def install_nvm():
    nvm_sh = os.path.join(HOME, ".nvm", "nvm.sh")
    if not os.path.isfile(nvm_sh):
        print("[nvm] Installing nvm")
        run("curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash")
    else:
        print("[nvm] Already installed")
    write_file(os.path.join(BASHRC_D, "nvm.sh"),
               'export NVM_DIR="$HOME/.nvm"\n'
               '[ -s "$NVM_DIR/nvm.sh" ] && \\. "$NVM_DIR/nvm.sh"\n'
               '[ -s "$NVM_DIR/bash_completion" ] && \\. "$HOME/.nvm/bash_completion"\n')
    write_file(os.path.join(FISH_CONFD, "nvm.fish"),
               'set -gx NVM_DIR "$HOME/.nvm"\n'
               'if test -d "$NVM_DIR"\n'
               '    if test -f "$NVM_DIR/alias/default"\n'
               '        set -l default_ver (cat "$NVM_DIR/alias/default")\n'
               '        for ver_dir in $NVM_DIR/versions/node/v$default_ver*\n'
               '            if test -d "$ver_dir/bin"\n'
               '                fish_add_path "$ver_dir/bin"\n'
               '                break\n'
               '            end\n'
               '        end\n'
               '    end\n'
               'end\n'
               '\n'
               'function nvm\n'
               '    set -gx NVM_DIR "$HOME/.nvm"\n'
               '    set -l cmd "source \\$NVM_DIR/nvm.sh && nvm $argv && echo \\"__ENV_START__\\" && env"\n'
               '    set -l res (bash -c "$cmd")\n'
               '    set -l in_env 0\n'
               '    for line in $res\n'
               '        if test "$line" = "__ENV_START__"\n'
               '            set in_env 1\n'
               '            continue\n'
               '        end\n'
               '        if test $in_env -eq 1\n'
               '            set -l kv (string split -m 1 "=" $line)\n'
               '            if test (count $kv) -eq 2\n'
               '                set -l key $kv[1]\n'
               '                set -l val $kv[2]\n'
               '                if string match -q "NVM_*" "$key"; or string match -q "NODE_*" "$key"; or test "$key" = "PATH"\n'
               '                    if test "$key" = "PATH"\n'
               '                        set -l path_list (string split ":" $val)\n'
               '                        set -gx PATH $path_list\n'
               '                    else\n'
               '                        set -gx $key $val\n'
               '                    end\n'
               '                end\n'
               '            end\n'
               '        else\n'
               '            echo "$line"\n'
               '        end\n'
               '    end\n'
               'end\n')


def install_pnpm():
    pnpm_bin = os.path.join(HOME, ".local", "share", "pnpm", "bin", "pnpm")
    if not os.path.isfile(pnpm_bin):
        print("[pnpm] Installing pnpm")
        run("export NVM_DIR=\"$HOME/.nvm\" && [ -s \"$NVM_DIR/nvm.sh\" ] && . \"$NVM_DIR/nvm.sh\" && npm install -g pnpm")
    else:
        print("[pnpm] Already installed")
    write_file(os.path.join(BASHRC_D, "pnpm.sh"),
               'export PNPM_HOME="$HOME/.local/share/pnpm"\n'
               'case ":$PATH:" in\n'
               '  *":$PNPM_HOME/bin:"*) ;;\n'
               '  *) export PATH="$PNPM_HOME/bin:$PATH" ;;\n'
               'esac\n')
    write_file(os.path.join(FISH_CONFD, "pnpm.fish"),
               'set -gx PNPM_HOME "$HOME/.local/share/pnpm"\n'
               'if test -d "$PNPM_HOME"\n'
               '    fish_add_path "$PNPM_HOME/bin"\n'
               'end\n')


def install_rustup():
    cargo_bin = os.path.join(HOME, ".cargo", "bin", "cargo")
    if not os.path.isfile(cargo_bin):
        print("[rust] Installing rustup")
        run("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y")
    else:
        print("[rust] Already installed")
    write_file(os.path.join(BASHRC_D, "cargo.sh"),
               'if [ -f "$HOME/.cargo/env" ]; then\n'
               '    . "$HOME/.cargo/env"\n'
               'fi\n')
    write_file(os.path.join(FISH_CONFD, "cargo.fish"),
               'if test -d "$HOME/.cargo/bin"\n'
               '    fish_add_path "$HOME/.cargo/bin"\n'
               'end\n')


def install_opencode():
    opencode_bin = os.path.join(HOME, ".opencode", "bin", "opencode")
    if not os.path.isfile(opencode_bin):
        print("[opencode] Installing opencode")
        run("mkdir -p \"$HOME/.opencode/bin\" && curl -fsSL https://opencode.ai/install | sh")
    else:
        print("[opencode] Already installed")
    write_file(os.path.join(BASHRC_D, "opencode.sh"),
               'export PATH="$HOME/.opencode/bin:$PATH"\n')
    write_file(os.path.join(FISH_CONFD, "opencode.fish"),
               'if test -d "$HOME/.opencode/bin"\n'
               '    fish_add_path "$HOME/.opencode/bin"\n'
               'end\n')


def install_sdkman():
    sdkman_init = os.path.join(HOME, ".sdkman", "bin", "sdkman-init.sh")
    if not os.path.isfile(sdkman_init):
        print("[sdkman] Installing sdkman")
        run("curl -s \"https://get.sdkman.io\" | bash")
    else:
        print("[sdkman] Already installed")
    write_file(os.path.join(BASHRC_D, "sdkman.sh"),
               'export SDKMAN_DIR="$HOME/.sdkman"\n'
               '[[ -s "$SDKMAN_DIR/bin/sdkman-init.sh" ]] && source "$SDKMAN_DIR/bin/sdkman-init.sh"\n')
    write_file(os.path.join(FISH_CONFD, "sdkman.fish"),
               'set -gx SDKMAN_DIR "$HOME/.sdkman"\n'
               'if test -d "$SDKMAN_DIR"\n'
               '    for candidate_bin in $SDKMAN_DIR/candidates/*/current/bin\n'
               '        if test -d "$candidate_bin"\n'
               '            fish_add_path "$candidate_bin"\n'
               '        end\n'
               '    end\n'
               'end\n'
               '\n'
               'function sdk\n'
               '    set -gx SDKMAN_DIR "$HOME/.sdkman"\n'
               '    set -l cmd "source \\$SDKMAN_DIR/bin/sdkman-init.sh && sdk $argv && echo \\"__ENV_START__\\" && env"\n'
               '    set -l res (bash -c "$cmd")\n'
               '    set -l in_env 0\n'
               '    for line in $res\n'
               '        if test "$line" = "__ENV_START__"\n'
               '            set in_env 1\n'
               '            continue\n'
               '        end\n'
               '        if test $in_env -eq 1\n'
               '            set -l kv (string split -m 1 "=" $line)\n'
               '            if test (count $kv) -eq 2\n'
               '                set -l key $kv[1]\n'
               '                set -l val $kv[2]\n'
               '                if string match -q "SDKMAN_*" "$key"; or test "$key" = "PATH"\n'
               '                    if test "$key" = "PATH"\n'
               '                        set -l path_list (string split ":" $val)\n'
               '                        set -gx PATH $path_list\n'
               '                    else\n'
               '                        set -gx $key $val\n'
               '                    end\n'
               '                end\n'
               '            end\n'
               '        else\n'
               '            echo "$line"\n'
               '        end\n'
               '    end\n'
               'end\n')


def main():
    steps = [
        ("Shell environment", setup_shell),
        ("nvm", install_nvm),
        ("pnpm", install_pnpm),
        ("Rustup", install_rustup),
        ("Opencode", install_opencode),
        ("SDKMAN", install_sdkman),
    ]
    for name, fn in steps:
        print(f"\n=== {name} ===")
        fn()
    print("\nDone. Restart your shell or run: exec fish")


if __name__ == "__main__":
    main()
