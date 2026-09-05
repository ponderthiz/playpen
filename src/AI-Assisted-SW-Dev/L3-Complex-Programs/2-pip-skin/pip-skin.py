import asyncio
import sys
from nicegui import ui

async def run_pip_command(cmd_args: list[str], log_view: ui.log, spinner: ui.spinner, buttons: list[ui.button]):
    """Executes a pip subprocess asynchronously and streams output line-by-line."""
    # Disable controls while command executes
    for btn in buttons:
        btn.disable()
    spinner.set_visibility(True)

    full_cmd = [sys.executable, "-m", "pip"] + cmd_args
    log_view.push(f"--- Running: pip {' '.join(cmd_args)} ---")

    try:
        process = await asyncio.create_subprocess_exec(
            *full_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

        while True:
            line = await process.stdout.readline()
            if not line:
                break
            log_view.push(line.decode().rstrip())

        await process.wait()

        if process.returncode == 0:
            ui.notify("Command completed successfully", type="positive")
            log_view.push("--- Command Finished ---\n")
        else:
            ui.notify(f"Command failed (exit code {process.returncode})", type="negative")
            log_view.push(f"--- Failed with code {process.returncode} ---\n")

    except Exception as e:
        ui.notify(f"Execution error: {e}", type="negative")
        log_view.push(f"Error: {e}\n")
    finally:
        spinner.set_visibility(False)
        for btn in buttons:
            btn.enable()


# --- UI Layout ---
with ui.card().classes("w-full max-w-2xl mx-auto mt-8 p-6 shadow-md"):
    ui.label("Pip Package Manager").classes("text-2xl font-bold text-gray-800")
    ui.label("Manage packages in your current Codespaces environment.").classes("text-sm text-gray-500 mb-4")

    # Install input row
    with ui.row().classes("w-full items-center gap-2"):
        pkg_input = ui.input(
            label="Package Name", 
            placeholder="e.g. requests, pandas==2.0.0"
        ).classes("flex-grow")
        
        upgrade_checkbox = ui.checkbox("Upgrade (-U)").props("dense")

    # Action buttons row
    with ui.row().classes("items-center gap-3 mt-2"):
        loading_spinner = ui.spinner(size="md").props("color=primary")
        loading_spinner.set_visibility(False)

        async def start_install():
            pkg = pkg_input.value.strip()
            if not pkg:
                ui.notify("Please enter a package name", type="warning")
                return

            args = ["install"]
            if upgrade_checkbox.value:
                args.append("-U")
            # Split in case user supplied multiple packages or flags
            args.extend(pkg.split())
            
            await run_pip_command(args, output_log, loading_spinner, [install_btn, list_btn, clear_btn])

        async def start_list():
            output_log.clear()
            await run_pip_command(["list"], output_log, loading_spinner, [install_btn, list_btn, clear_btn])

        install_btn = ui.button("Install Package", icon="download", on_click=start_install).props("unelevated color=primary")
        list_btn = ui.button("List Installed", icon="list", on_click=start_list).props("outline color=secondary")
        clear_btn = ui.button("Clear Log", icon="delete", on_click=lambda: output_log.clear()).props("flat color=grey")

    # Shared Terminal Output Window
    ui.label("Output Window").classes("text-sm font-semibold text-gray-700 mt-4")
    output_log = ui.log(max_lines=1000).classes("w-full h-72 bg-gray-950 text-gray-100 p-3 rounded font-mono text-xs overflow-y-auto")

ui.run(host="0.0.0.0", port=8080, title="Pip Manager")