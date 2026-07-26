"""
WEBSTER — Workspace for Enhanced Business, Study, Technology, Engineering & Research
===================================================================================
Main entry point for the WEBSTER ecosystem.

Usage:
    python main.py                    # Launch GUI
    python main.py --headless         # Run services only (no GUI)
    python main.py --dashboard        # Launch with web dashboard
    python main.py --voice            # Enable voice from startup
    python main.py --mobile           # Enable mobile API server
"""

import sys
import os
import signal
import argparse
import logging
import threading
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from webster.config.branding import APP_NAME, VERSION, AI_NAME, ENGINE_NAME


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=f"{APP_NAME} v{VERSION} — Your AI Operating System"
    )
    parser.add_argument("--headless", action="store_true",
                       help="Run without GUI")
    parser.add_argument("--dashboard", action="store_true",
                       help="Start web dashboard")
    parser.add_argument("--voice", action="store_true",
                       help="Enable voice from startup")
    parser.add_argument("--mobile", action="store_true",
                       help="Start mobile API server")
    parser.add_argument("--debug", action="store_true",
                       help="Enable debug logging")
    return parser.parse_args()


def setup_logging(debug: bool = False):
    """Configure logging for the application."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%H:%M:%S"
    )
    return logging.getLogger(APP_NAME)


def print_banner():
    """Display startup banner."""
    banner = f"""
    ╔══════════════════════════════════════════╗
    ║          {APP_NAME:^30s}           ║
    ║     v{VERSION}                           ║
    ║                                          ║
    ║  🕷️ {AI_NAME:31s}║
    ║  ⚡ {ENGINE_NAME:30s}║
    ╚══════════════════════════════════════════╝
    """
    print(banner)


def run_headless(args, logger):
    """Run WEBSTER in headless mode with all services."""
    logger.info("Starting WEBSTER in headless mode...")
    print_banner()

    from webster.core.brain import HelvacEngine
    from webster.core.assistant import SpideyAssistant
    from webster.core.memory import MemoryManager
    from webster.memory.sqlite_store import SQLiteStore

    logger.info("Initializing services...")

    # Initialize core systems
    sqlite = SQLiteStore()
    memory = MemoryManager()
    helvac = HelvacEngine()
    spidey = SpideyAssistant(helvac=helvac, memory=memory)
    spidey.activate()

    logger.info("All services initialized.")
    logger.info(f"{AI_NAME} is ready. Type 'exit' to quit.")

    # Start dashboard if requested
    dashboard_thread = None
    if args.dashboard:
        from webster.dashboard.server import DashboardServer
        dashboard = DashboardServer()
        dashboard_thread = dashboard.start_background()

    # Start mobile server if requested
    mobile_thread = None
    if args.mobile:
        from webster.mobile.server import MobileServer
        mobile = MobileServer()
        mobile_thread = mobile.start_background()

    # Start voice if requested
    if args.voice:
        from webster.voice.controller import VoiceController
        vc = VoiceController()
        vc.start_listening()
        logger.info("Voice enabled")

    # Interactive REPL
    try:
        while True:
            try:
                user_input = input(f"\n[{AI_NAME}] You: ").strip()
                if user_input.lower() in ("exit", "quit", "bye"):
                    print(f"[{AI_NAME}] Goodbye! 🕷️")
                    break
                if not user_input:
                    continue

                response = spidey.process_message(user_input)
                print(f"[{AI_NAME}] {response}")

            except (KeyboardInterrupt, EOFError):
                print(f"\n[{AI_NAME}] Shutting down gracefully...")
                break

    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        logger.info("WEBSTER shutdown complete.")


def run_gui(args, logger):
    """Launch WEBSTER GUI application."""
    logger.info(f"Starting {APP_NAME} GUI...")
    print_banner()

    from webster.core.brain import HelvacEngine
    from webster.core.assistant import SpideyAssistant
    from webster.core.memory import MemoryManager
    from webster.memory.sqlite_store import SQLiteStore
    from webster.ui.app import WebsterApp

    logger.info("Initializing WEBSTER services...")

    # Initialize core systems
    sqlite = SQLiteStore()
    memory = MemoryManager()
    helvac = HelvacEngine()
    spidey = SpideyAssistant(helvac=helvac, memory=memory)
    spidey.activate()

    # Start background services
    dashboard_thread = None
    if args.dashboard:
        from webster.dashboard.server import DashboardServer
        dashboard = DashboardServer()
        dashboard_thread = dashboard.start_background()
        logger.info("Web dashboard started on port 8765")

    mobile_thread = None
    if args.mobile:
        from webster.mobile.server import MobileServer
        mobile = MobileServer()
        mobile_thread = mobile.start_background()
        logger.info("Mobile API started on port 8766")

    if args.voice:
        from webster.voice.controller import VoiceController
        vc = VoiceController()
        vc.start_listening()
        logger.info("Voice enabled")

    # Launch GUI
    logger.info(f"Launching {APP_NAME} UI...")
    app = WebsterApp(helvac=helvac, spidey=spidey)
    app.run()


def main():
    """Main entry point."""
    args = parse_args()
    logger = setup_logging(debug=args.debug)

    logger.info(f"{APP_NAME} v{VERSION} starting...")
    logger.info(f"AI: {AI_NAME} | Engine: {ENGINE_NAME}")

    try:
        if args.headless:
            run_headless(args, logger)
        else:
            run_gui(args, logger)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
