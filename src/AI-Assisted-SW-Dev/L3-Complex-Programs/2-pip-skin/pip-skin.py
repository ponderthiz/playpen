import asyncio
import sys
from nicegui import ui

async def run_pip_command(action: str, package: str, log_view: ui.log, spinner: ui.spinner, btn: ui.button):
    """Executes a pip subprocess asynchronously and streams output line-by-line."""
    pkg = package.strip()
    if not pkg:
        ui.notify("Please enter a package name", type="warning")
        return

    # Disable the install button and show spinner
    btn.disable()
    spinner.set_visibility(True)
    log_view.push(f"--- Running: pip {action} {pkg} ---")

    cmd = [sys.executable, "-m", "pip", action, pkg]

    try:
        # Start the subprocess asynchronously to keep the UI responsive
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

        # Read output stream line-by-line in real time
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            log_view.push(line.decode().rstrip())

        await process.wait()

        if process.returncode == 0:
            ui.notify(f"Successfully finished: {pkg}", type="positive")
            log_view.push("--- Command Succeeded ---\n")
        else:
            ui.notify(f"Command failed (exit code {process.returncode})", type="negative")
            log_view.push(f"--- Failed with code {process.returncode} ---\n")

    except Exception as e:
        ui.notify(f"Execution error: {e}", type="negative")
        log_view.push(f"Error: {e}\n")
    finally:
        spinner.set_visibility(False)
        btn.enable()


# --- UI Layout ---
with ui.card().classes("w-full max-w-2xl mx-auto mt-8 p-6 shadow-md"):
    ui.label("Pip Package Manager").classes("text-2xl font-bold text-gray-800")
    ui.label("Install or upgrade packages into your current Codespaces environment.").classes("text-sm text-gray-500 mb-4")

    with ui.row().classes("w-full items-center gap-2"):
        pkg_input = ui.input(
            label="Package Name", 
            placeholder="e.g. requests, pandas==2.0.0"
        ).classes("flex-grow")
        
        upgrade_checkbox = ui.checkbox("Upgrade (-U)").props("dense")

    with ui.row().classes("items-center gap-3 mt-2"):
        loading_spinner = ui.spinner(size="md").props("color=primary")
        loading_spinner.set_visibility(False)

        async def start_install():
            action = "install"
            target = f"-U {pkg_input.value}" if upgrade_checkbox.value else pkg_input.value
            await run_pip_command(action, target, output_log, loading_spinner, install_btn)

        install_btn = ui.button("Install Package", icon="download", on_click=start_install).props("unelevated color=primary")

    # Terminal output viewer
    ui.label("Terminal Output").classes("text-sm font-semibold text-gray-700 mt-4")
    output_log = ui.log(max_lines=500).classes("w-full h-64 bg-gray-950 text-gray-100 p-3 rounded font-mono text-xs overflow-y-auto")

# 0.0.0.0 binds to all interfaces, which Codespaces port forwarding requires
ui.run(host="0.0.0.0", port=8080, title="Pip Manager")
