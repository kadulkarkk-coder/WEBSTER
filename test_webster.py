"""WEBSTER End-to-End System Test"""
import sys, os, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("=" * 50)
print("WEBSTER System Test")
print("=" * 50)

from webster.config.branding import APP_NAME, VERSION, AI_NAME, ENGINE_NAME, WAKE_WORD
from webster.core.brain import HelvacEngine, Task, TaskType
from webster.core.assistant import SpideyAssistant
from webster.core.memory import MemoryManager
from webster.memory.sqlite_store import SQLiteStore
from webster.core.scheduler import Scheduler
from webster.core.events import EventBus
from webster.core.router import RequestRouter, RouteTarget
from webster.core.logger import Logger
from webster.core.errors import WebsterError, ConfigError, AIError, VoiceError, MemoryError
from webster.ai.provider_manager import ProviderManager
from webster.voice.controller import VoiceController
from webster.study.notes import NotesManager
from webster.study.flashcards import FlashcardManager
from webster.study.quiz import QuizGenerator
from webster.automation.browser import BrowserController
from webster.automation.files import FileManager
from webster.widgets.manager import WidgetManager
from webster.plugins.manager import PluginManager
from webster.sync.manager import SyncManager

# Initialize all systems
print("\nInitializing systems...")
sqlite = SQLiteStore()
memory = MemoryManager()
helvac = HelvacEngine()
spidey = SpideyAssistant(helvac=helvac, memory=memory)
scheduler = Scheduler()
events = EventBus()
router = RequestRouter()
provider_mgr = ProviderManager()
voice = VoiceController()
notes = NotesManager()
flashcards = FlashcardManager()
quiz = QuizGenerator()
browser = BrowserController()
file_auto = FileManager()
widgets = WidgetManager()
plugins = PluginManager()
sync = SyncManager()

# Activate Spidey
spidey.activate()

# Register modules with HELVAC
helvac.register_module('ai', provider_mgr)
helvac.register_module('study', notes)
helvac.register_module('voice', voice)

# Tests
print("\nRunning tests...")
tests_passed = 0
tests_failed = 0

def test(name, condition):
    global tests_passed, tests_failed
    if condition:
        print(f"  ✓ {name}")
        tests_passed += 1
    else:
        print(f"  ✗ {name}")
        tests_failed += 1

# Core tests
test("Spidey active", spidey.is_active)
test("Wake word 'hey spidey'", spidey.check_wake_word('hey spidey'))
test("Wake word 'Hey Spidey!'", spidey.check_wake_word('Hey Spidey!'))
test("No false wake word", not spidey.check_wake_word('hello world'))

# Router tests
result = router.route('study python flashcards')
test("Route study", result.target == RouteTarget.STUDY)
result = router.route('open browser')
test("Route automation", result.target == RouteTarget.AUTOMATION)
result = router.route('what is AI')
test("Route default AI", result.target == RouteTarget.AI)

# Scheduler tests
task_id = scheduler.schedule_once('test', lambda: None, 1)
test("Scheduler creates tasks", task_id is not None)

# Memory tests
memory.add_user_message('Hello Spidey')
memory.add_assistant_message('Hi there! How can I help?')
stats = memory.memory_stats()
test("Memory stores messages", stats['total_messages'] >= 2)
test("Memory has conversations", stats['conversations'] >= 1)

# HELVAC tests
test("HELVAC has modules", len(helvac.list_modules()) >= 1)
test("HELVAC can analyze", helvac.analyze_task(Task(id="t1", type=TaskType.UNKNOWN, input="study python")) == TaskType.STUDY)

# Voice tests
voice.enable()
test("Voice enabled", voice.is_enabled)
voice.disable()
test("Voice disabled", not voice.is_enabled)

# Notes tests
note_id = notes.create("Test Note", "This is a test note", "test")
test("Notes create", note_id is not None)
test("Notes get all", len(notes.get_all()) >= 1)

# Flashcard tests
card_id = flashcards.create("Q: What is Python?", "A: A programming language", "programming")
test("Flashcards create", card_id is not None)

# Quiz tests
q = quiz.multiple_choice("What is 2+2?", ["3", "4", "5", "6"], 1)
test("Quiz creates MC question", q is not None)

# Browser tests
test("Browser controller", browser is not None)

# File tests
file_auto.create_file("test_temp.txt", "hello world")
test("File create", os.path.exists("test_temp.txt"))
file_auto.delete("test_temp.txt")
test("File delete", not os.path.exists("test_temp.txt"))

# Widget tests
test("Widget manager", widgets is not None)

# Plugin tests
test("Plugin manager", plugins is not None)

# Sync tests
test("Sync manager", sync is not None)

# Router targets
available = router.get_available_targets()
test(f"Router has {len(available)} targets", len(available) >= 5)

# Report
print(f"\n{'=' * 50}")
print(f"Results: {tests_passed} passed, {tests_failed} failed")
print(f"{'=' * 50}")
print(f"\n{APP_NAME} v{VERSION}")
print(f"AI: {AI_NAME} | Engine: {ENGINE_NAME} | Wake Word: \"{WAKE_WORD}\"")
print(f"HELVAC modules: {helvac.list_modules()}")
print(f"Router targets: {available}")
print(f"Memory stats: {stats}")
print(f"\n✓ System is {'OPERATIONAL' if tests_failed == 0 else 'PARTIALLY OPERATIONAL'}!")
