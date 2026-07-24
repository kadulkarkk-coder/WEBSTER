import customtkinter as ctk
import threading
import time

from tkinter import filedialog
from pathlib import Path

from aura.theme.theme import Theme

from aura.ui.widgets.glass_frame import GlassFrame
from aura.ui.widgets.glass_button import GlassButton
from aura.ui.widgets.glass_bar import GlassBar
from aura.ui.widgets.glass_entry import GlassEntry
from aura.ui.widgets.glass_title import GlassTitle
from aura.ui.widgets.glass_separator import GlassSeparator
from aura.ui.widgets.glass_icon import GlassIcon

from backend.pipelines.upload_pipeline import UploadPipeline
from backend.pipelines.generation_pipeline import GenerationPipeline
from backend.pipelines.preview_pipeline import PreviewPipeline
from backend.pipelines.export_pipeline import ExportPipeline
from backend.projects.project_manager import ProjectManager

from backend.generators.notes_generator import NotesGenerator
from backend.generators.summary_generator import SummaryGenerator
from backend.generators.quiz_generator import QuizGenerator
from backend.generators.flashcard_generator import FlashcardGenerator
from backend.generators.worksheet_generator import WorksheetGenerator
from backend.generators.mindmap_generator import MindMapGenerator
from backend.generators.speech_generator import SpeechGenerator
from backend.generators.ppt_generator import PPTGenerator
from backend.generators.question_paper_generator import QuestionPaperGenerator


class StudyHubPage(
    ctk.CTkFrame
):

    """
    ==================================================

                    WEBSTER Study Hub

    ==================================================

    Sprint 24

    AI Powered Study Workspace

        • PDF Analysis

        • Chapter Notes

        • Summaries

        • Flashcards

        • Mind Maps

        • Question Papers

        • Worksheets

        • Presentations

        • Speech Writing

        • Project Management

    ==================================================
    """

    # ==================================================
    # Constructor
    # ==================================================

    def __init__(

        self,

        master,

        controller,

        ai_engine

    ):

        super().__init__(

            master,

            fg_color=Theme.Colors.BACKGROUND

        )

        self.controller = controller

        self.ai_engine = ai_engine

        # ==================================================
        # Backend
        # ==================================================

        self.upload_pipeline = UploadPipeline()

        self.preview_pipeline = PreviewPipeline()

        self.export_pipeline = ExportPipeline()

        self.project_manager = ProjectManager()

        self.generation_pipeline = GenerationPipeline(

            ai_engine

        )

        # ==================================================
        # Current State
        # ==================================================

        self.current_document = None

        self.current_result = None

        self.current_project = None

        self.current_generator = None

        self.current_file = ""

        # ==================================================
        # Generators
        # ==================================================

        self.generators = {

            "Notes": NotesGenerator(),

            "Summary": SummaryGenerator(),

            "Quiz": QuizGenerator(),

            "Flashcards": FlashcardGenerator(),

            "Worksheet": WorksheetGenerator(),

            "Mind Map": MindMapGenerator(),

            "Speech": SpeechGenerator(),

            "Presentation": PPTGenerator(),

            "Question Paper": QuestionPaperGenerator()

        }

        # ==================================================
        # Layout Variables
        # ==================================================

        self.toolbar = None

        self.workspace = None

        self.preview = None

        self.statusbar = None

        self.preview_box = None

        self.prompt_box = None

        self.file_label = None

        self.progress_bar = None

        self.status_label = None

        # ==================================================
        # Build
        # ==================================================

        self.build()

    # ==================================================
    # Build
    # ==================================================

    def build(

        self

    ):

        self.grid_rowconfigure(

            1,

            weight=1

        )

        self.grid_columnconfigure(

            1,

            weight=1

        )

        self._build_toolbar()

        self._build_workspace()

        self._build_statusbar()

    # ==================================================
    # Toolbar
    # ==================================================

    def _build_toolbar(

        self

    ):

        self.toolbar = GlassFrame(

            self,

            width=300

        )

        self.toolbar.grid(

            row=1,

            column=0,

            sticky="ns",

            padx=(20, 10),

            pady=(15, 15)

        )

        self.toolbar.grid_propagate(

            False

        )

        GlassTitle(

            self.toolbar,

            text="Study Hub"

        ).pack(

            anchor="w",

            padx=20,

            pady=(20, 8)

        )

        GlassSeparator(

            self.toolbar

        ).pack(

            fill="x",

            padx=18,

            pady=(0, 18)

        )

        self.tool_scroll = ctk.CTkScrollableFrame(

            self.toolbar,

            fg_color="transparent"

        )

        self.tool_scroll.pack(

            fill="both",

            expand=True,

            padx=12,

            pady=5

        )

        self.tool_buttons = {}

        self.tool_config = [

            (

                "Upload",

                "upload",

                self.upload_document

            ),

            (

                "Notes",

                "notes",

                self.generate_notes

            ),

            (

                "Summary",

                "summary",

                self.generate_summary

            ),

            (

                "Quiz",

                "quiz",

                self.generate_quiz

            ),

            (

                "Flashcards",

                "flashcards",

                self.generate_flashcards

            ),

            (

                "Worksheet",

                "worksheet",

                self.generate_worksheet

            ),

            (

                "Mind Map",

                "mindmap",

                self.generate_mindmap

            ),

            (

                "Speech",

                "speech",

                self.generate_speech

            ),

            (

                "Presentation",

                "presentation",

                self.generate_presentation

            ),

            (

                "Question Paper",

                "question_paper",

                self.generate_question_paper

            )

        ]

        for title, text, command in self.tool_config:

            button = GlassButton(

                self.tool_scroll,

                text=title,

                text=text,

                command=command,

                height=44

            )

            button.pack(

                fill="x",

                pady=5

            )

            self.tool_buttons[

                title

            ] = button

        GlassSeparator(

            self.tool_scroll

        ).pack(

            fill="x",

            pady=20

        )

        self.project_buttons = [

            (

                "New Project",

                self.new_project

            ),

            (

                "Open Project",

                self.open_project

            ),

            (

                "Save Project",

                self.save_project

            ),

            (

                "Export",

                self.export_result

            ),

            (

                "Clear",

                self.clear_workspace

            )

        ]

        for text, command in self.project_buttons:

            GlassButton(

                self.tool_scroll,

                text=text,

                command=command,

                height=42

            ).pack(

                fill="x",

                pady=4

            )

    # ==================================================
    # Workspace
    # ==================================================

    def _build_workspace(

        self

    ):

        self.workspace = GlassFrame(

            self

        )

        self.workspace.grid(

            row=1,

            column=1,

            sticky="nsew",

            padx=(5, 20),

            pady=(15, 15)

        )

        self.workspace.grid_rowconfigure(

            2,

            weight=1

        )

        self.workspace.grid_columnconfigure(

            0,

            weight=1

        )

        # ==================================================
        # Header
        # ==================================================

        self.workspace_title = GlassTitle(

            self.workspace,

            text="AI Study Workspace"

        )

        self.workspace_title.grid(

            row=0,

            column=0,

            sticky="w",

            padx=20,

            pady=(20, 8)

        )

        self.workspace_separator = GlassSeparator(

            self.workspace

        )

        self.workspace_separator.grid(

            row=1,

            column=0,

            sticky="ew",

            padx=20,

            pady=(0, 15)

        )

        # ==================================================
        # Main Body
        # ==================================================

        self.body = ctk.CTkFrame(

            self.workspace,

            fg_color="transparent"

        )

        self.body.grid(

            row=2,

            column=0,

            sticky="nsew",

            padx=18,

            pady=(0, 18)

        )

        self.body.grid_columnconfigure(

            0,

            weight=2

        )

        self.body.grid_columnconfigure(

            1,

            weight=3

        )

        self.body.grid_rowconfigure(

            0,

            weight=1

        )

        self._build_prompt_panel()

        self._build_preview_panel()

    # ==================================================
    # Prompt Panel
    # ==================================================

    def _build_prompt_panel(

        self

    ):

        self.prompt_panel = GlassFrame(

            self.body

        )

        self.prompt_panel.grid(

            row=0,

            column=0,

            sticky="nsew",

            padx=(0, 8)

        )

        self.prompt_panel.grid_rowconfigure(

            3,

            weight=1

        )

        self.prompt_panel.grid_columnconfigure(

            0,

            weight=1

        )

        GlassTitle(

            self.prompt_panel,

            text="Instructions"

        ).grid(

            row=0,

            column=0,

            sticky="w",

            padx=18,

            pady=(18, 10)

        )

        self.prompt_box = ctk.CTkTextbox(

            self.prompt_panel,

            font=(

                "Segoe UI",

                14

            ),

            wrap="word",

            border_width=0

        )

        self.prompt_box.grid(

            row=1,

            column=0,

            sticky="nsew",

            padx=18,

            pady=(0, 15)

        )

        self.prompt_box.insert(

            "1.0",

            "Type additional instructions for the AI...\n\n"
            "Examples:\n"
            "• Create topper notes\n"
            "• Make revision points\n"
            "• Include diagrams\n"
            "• Explain in simple language"

        )

        self.prompt_actions = ctk.CTkFrame(

            self.prompt_panel,

            fg_color="transparent"

        )

        self.prompt_actions.grid(

            row=2,

            column=0,

            sticky="ew",

            padx=18,

            pady=(0, 15)

        )

        GlassButton(

            self.prompt_actions,

            text="Clear Prompt",

            command=self.clear_prompt

        ).pack(

            side="left",

            padx=(0, 8)

        )

        GlassButton(

            self.prompt_actions,

            text="Reset",

            command=self.reset_prompt

        ).pack(

            side="left"

        )

    # ==================================================
    # Preview Panel
    # ==================================================

    def _build_preview_panel(

        self

    ):

        self.preview = GlassFrame(

            self.body

        )

        self.preview.grid(

            row=0,

            column=1,

            sticky="nsew",

            padx=(8, 0)

        )

        self.preview.grid_rowconfigure(

            2,

            weight=1

        )

        self.preview.grid_columnconfigure(

            0,

            weight=1

        )

        GlassTitle(

            self.preview,

            text="Preview"

        ).grid(

            row=0,

            column=0,

            sticky="w",

            padx=18,

            pady=(18, 10)

        )

        self.preview_tabs = ctk.CTkSegmentedButton(

            self.preview,

            values=[

                "Output",

                "Markdown",

                "Statistics",

                "Raw"

            ]

        )

        self.preview_tabs.grid(

            row=1,

            column=0,

            sticky="ew",

            padx=18,

            pady=(0, 12)

        )

        self.preview_tabs.set(

            "Output"

        )

        self.preview_box = ctk.CTkTextbox(

            self.preview,

            wrap="word",

            font=(

                "Segoe UI",

                14

            ),

            border_width=0

        )

        self.preview_box.grid(

            row=2,

            column=0,

            sticky="nsew",

            padx=18,

            pady=(0, 18)

        )

        self.preview_box.insert(

            "1.0",

            "Your generated study material will appear here..."

        )

        self.preview_box.configure(

            state="disabled"

        )

    # ==================================================
    # Status Bar
    # ==================================================

    def _build_statusbar(

        self

    ):

        self.statusbar = GlassBar(

            self

        )

        self.statusbar.grid(

            row=2,

            column=0,

            columnspan=2,

            sticky="ew",

            padx=20,

            pady=(0, 20)

        )

        self.statusbar.grid_columnconfigure(

            1,

            weight=1

        )

        self.statusbar.grid_columnconfigure(

            2,

            weight=1

        )

        self.statusbar.grid_columnconfigure(

            3,

            weight=1

        )

        # ==================================================
        # Left
        # ==================================================

        self.status_left = ctk.CTkFrame(

            self.statusbar,

            fg_color="transparent"

        )

        self.status_left.grid(

            row=0,

            column=0,

            padx=(20, 10),

            pady=12,

            sticky="w"

        )

        self.file_label = ctk.CTkLabel(

            self.status_left,

            text="No document loaded",

            anchor="w"

        )

        self.file_label.pack(

            anchor="w"

        )

        self.generator_label = ctk.CTkLabel(

            self.status_left,

            text="Generator : None",

            anchor="w"

        )

        self.generator_label.pack(

            anchor="w"

        )

        # ==================================================
        # Center
        # ==================================================

        self.status_center = ctk.CTkFrame(

            self.statusbar,

            fg_color="transparent"

        )

        self.status_center.grid(

            row=0,

            column=1,

            padx=20,

            pady=10,

            sticky="ew"

        )

        self.progress_bar = ctk.CTkProgressBar(

            self.status_center,

            height=10

        )

        self.progress_bar.pack(

            fill="x"

        )

        self.progress_bar.set(

            0

        )

        self.status_label = ctk.CTkLabel(

            self.status_center,

            text="Ready"

        )

        self.status_label.pack(

            pady=(6, 0)

        )

        # ==================================================
        # Right
        # ==================================================

        self.status_right = ctk.CTkFrame(

            self.statusbar,

            fg_color="transparent"

        )

        self.status_right.grid(

            row=0,

            column=2,

            padx=20,

            pady=10,

            sticky="e"

        )

        self.project_label = ctk.CTkLabel(

            self.status_right,

            text="Project : Untitled"

        )

        self.project_label.pack(

            anchor="e"

        )

        self.results_label = ctk.CTkLabel(

            self.status_right,

            text="Results : 0"

        )

        self.results_label.pack(

            anchor="e"

        )

        # ==================================================
        # AI Status
        # ==================================================

        self.ai_status = ctk.CTkFrame(

            self.statusbar,

            fg_color="transparent"

        )

        self.ai_status.grid(

            row=0,

            column=3,

            padx=(10, 20),

            pady=10,

            sticky="e"

        )

        self.ai_indicator = ctk.CTkLabel(

            self.ai_status,

            text="●",

            text_color="#00D26A",

            font=(

                "Segoe UI",

                16,

                "bold"

            )

        )

        self.ai_indicator.pack(

            side="left",

            padx=(0, 8)

        )

        self.ai_label = ctk.CTkLabel(

            self.ai_status,

            text="AI Ready"

        )

        self.ai_label.pack(

            side="left"

        )

    # ==================================================
    # Status Helpers
    # ==================================================

    def set_status(

        self,

        text

    ):

        self.status_label.configure(

            text=text

        )

    def set_progress(

        self,

        value

    ):

        value = max(

            0,

            min(

                1,

                value

            )

        )

        self.progress_bar.set(

            value

        )

    def set_current_file(

        self,

        file

    ):

        self.current_file = file

        self.file_label.configure(

            text=Path(

                file

            ).name

        )

    def set_generator(

        self,

        name

    ):

        self.generator_label.configure(

            text=f"Generator : {name}"

        )

    def set_project(

        self,

        name

    ):

        self.project_label.configure(

            text=f"Project : {name}"

        )

    def set_results(

        self,

        count

    ):

        self.results_label.configure(

            text=f"Results : {count}"

        )

    def ai_busy(

        self

    ):

        self.ai_indicator.configure(

            text_color="#F59E0B"

        )

        self.ai_label.configure(

            text="Generating..."

        )

    def ai_ready(

        self

    ):

        self.ai_indicator.configure(

            text_color="#00D26A"

        )

        self.ai_label.configure(

            text="AI Ready"

        )

    def ai_error(

        self

    ):

        self.ai_indicator.configure(

            text_color="#EF4444"

        )

        self.ai_label.configure(

            text="Generation Failed"

        )

    # ==================================================
    # Upload
    # ==================================================

    def upload_document(

        self

    ):

        file = filedialog.askopenfilename(

            title="Select Study Material",

            filetypes=[

                (

                    "Supported Files",

                    "*.pdf *.docx *.txt *.md *.pptx *.png *.jpg *.jpeg"

                ),

                (

                    "PDF",

                    "*.pdf"

                ),

                (

                    "Word",

                    "*.docx"

                ),

                (

                    "Text",

                    "*.txt"

                ),

                (

                    "Markdown",

                    "*.md"

                ),

                (

                    "PowerPoint",

                    "*.pptx"

                ),

                (

                    "Images",

                    "*.png *.jpg *.jpeg"

                ),

                (

                    "All Files",

                    "*.*"

                )

            ]

        )

        if not file:

            return

        self.load_document(

            file

        )

    # ==================================================
    # Load Document
    # ==================================================

    def load_document(

        self,

        path

    ):

        try:

            self.set_status(

                "Loading..."

            )

            self.set_progress(

                0.15

            )

            self.current_document = (

                self.upload_pipeline.process(

                    path

                )

            )

            self.current_file = path

            self.set_current_file(

                path

            )

            self.set_status(

                "Document Loaded"

            )

            self.set_progress(

                1

            )

            self.preview_document()

        except Exception as error:

            self.show_error(

                error

            )

    # ==================================================
    # Preview Document
    # ==================================================

    def preview_document(

        self

    ):

        if self.current_document is None:

            return

        self.preview_box.configure(

            state="normal"

        )

        self.preview_box.delete(

            "1.0",

            "end"

        )

        preview = (

            self.current_document.text[:5000]

        )

        self.preview_box.insert(

            "1.0",

            preview

        )

        self.preview_box.configure(

            state="disabled"

        )

    # ==================================================
    # Website
    # ==================================================

    def load_website(

        self,

        url

    ):

        try:

            self.current_document = (

                self.upload_pipeline.process(

                    url

                )

            )

            self.preview_document()

            self.set_status(

                "Website Loaded"

            )

        except Exception as error:

            self.show_error(

                error

            )

    # ==================================================
    # Drag & Drop
    # ==================================================

    def on_file_drop(

        self,

        event

    ):

        file = event.data

        file = file.replace(

            "{",

            ""

        )

        file = file.replace(

            "}",

            ""

        )

        self.load_document(

            file

        )

    # ==================================================
    # Reload
    # ==================================================

    def reload_document(

        self

    ):

        if not self.current_file:

            return

        self.load_document(

            self.current_file

        )

    # ==================================================
    # Clear
    # ==================================================

    def clear_workspace(

        self

    ):

        self.current_document = None

        self.current_result = None

        self.current_file = ""

        self.preview_pipeline.clear()

        self.preview_box.configure(

            state="normal"

        )

        self.preview_box.delete(

            "1.0",

            "end"

        )

        self.preview_box.configure(

            state="disabled"

        )

        self.file_label.configure(

            text="No document loaded"

        )

        self.status_label.configure(

            text="Ready"

        )

        self.progress_bar.set(

            0

        )

    # ==================================================
    # Error
    # ==================================================

    def show_error(

        self,

        error

    ):

        self.ai_error()

        self.set_progress(

            0

        )

        self.set_status(

            "Operation Failed"

        )

        self.preview_box.configure(

            state="normal"

        )

        self.preview_box.delete(

            "1.0",

            "end"

        )

        self.preview_box.insert(

            "1.0",

            str(

                error

            )

        )

        self.preview_box.configure(

            state="disabled"
        )

    # ==================================================
    # Generation
    # ==================================================

    def generate(

        self,

        generator_name

    ):

        if self.current_document is None:

            self.set_status(

                "Please upload a document first."

            )

            return

        try:

            self.ai_busy()

            self.set_progress(

                0.05

            )

            self.set_status(

                "Building prompt..."

            )

            self.current_generator = (

                generator_name

            )

            self.set_generator(

                generator_name

            )

            generator = self.generators.get(

                generator_name

            )

            if generator is None:

                raise ValueError(

                    f"Unknown generator: {generator_name}"

                )

            prompt = generator.build_prompt(

                self.current_document,

                instructions=self.prompt_box.get(

                    "1.0",

                    "end"

                ).strip()

            )

            self.set_progress(

                0.25

            )

            self.set_status(

                "Generating..."

            )

            response = self.generation_pipeline.generate(

                prompt

            )

            self.set_progress(

                0.80

            )

            self.current_result = (

                generator.process_response(

                    response,

                    self.current_document

                )

            )

            self.preview_pipeline.update(

                self.current_result.content,

                preview_type="text"

            )

            self.display_result()

            if self.current_project:

                self.current_project.add_result(

                    self.current_result

                )

                self.set_results(

                    len(

                        self.current_project.results

                    )

                )

            self.set_progress(

                1

            )

            self.ai_ready()

            self.set_status(

                "Generation Complete"

            )

        except Exception as error:

            self.show_error(

                error

            )

    # ==================================================
    # Display Result
    # ==================================================

    def display_result(

        self

    ):

        if self.current_result is None:

            return

        self.preview_box.configure(

            state="normal"

        )

        self.preview_box.delete(

            "1.0",

            "end"

        )

        self.preview_box.insert(

            "1.0",

            self.current_result.content

        )

        self.preview_box.configure(

            state="disabled"

        )

    # ==================================================
    # Notes
    # ==================================================

    def generate_notes(

        self

    ):

        self.generate(

            "Notes"

        )

    # ==================================================
    # Summary
    # ==================================================

    def generate_summary(

        self

    ):

        self.generate(

            "Summary"

        )

    # ==================================================
    # Quiz
    # ==================================================

    def generate_quiz(

        self

    ):

        self.generate(

            "Quiz"

        )

    # ==================================================
    # Flashcards
    # ==================================================

    def generate_flashcards(

        self

    ):

        self.generate(

            "Flashcards"

        )

    # ==================================================
    # Worksheet
    # ==================================================

    def generate_worksheet(

        self

    ):

        self.generate(

            "Worksheet"

        )

    # ==================================================
    # Mind Map
    # ==================================================

    def generate_mindmap(

        self

    ):

        self.generate(

            "Mind Map"

        )

    # ==================================================
    # Generation Settings
    # ==================================================

    def collect_generation_options(

        self

    ):

        options = {

            "instructions":

                self.prompt_box.get(

                    "1.0",

                    "end"

                ).strip(),

            "board":

                getattr(

                    self,

                    "selected_board",

                    "CBSE"

                ),

            "grade":

                getattr(

                    self,

                    "selected_grade",

                    "Class 10"

                ),

            "difficulty":

                getattr(

                    self,

                    "selected_difficulty",

                    "Medium"

                ),

            "language":

                getattr(

                    self,

                    "selected_language",

                    "English"

                )

        }

        return options

    # ==================================================
    # Speech
    # ==================================================

    def generate_speech(

        self

    ):

        self.generate(

            "Speech"

        )

    # ==================================================
    # Presentation
    # ==================================================

    def generate_presentation(

        self

    ):

        self.generate(

            "Presentation"

        )

    # ==================================================
    # Question Paper
    # ==================================================

    def generate_question_paper(

        self

    ):

        self.generate(

            "Question Paper"

        )

    # ==================================================
    # Preview Result
    # ==================================================

    def preview_result(

        self,

        result

    ):

        self.preview_box.configure(

            state="normal"

        )

        self.preview_box.delete(

            "1.0",

            "end"

        )

        self.preview_box.insert(

            "1.0",

            result.content

        )

        self.preview_box.configure(

            state="disabled"

        )

    # ==================================================
    # Statistics
    # ==================================================

    def update_statistics(

        self,

        result

    ):

        words = len(

            result.content.split()

        )

        characters = len(

            result.content

        )

        lines = len(

            result.content.splitlines()

        )

        self.statistics = {

            "words": words,

            "characters": characters,

            "lines": lines,

            "generator": result.generator

        }

    # ==================================================
    # History
    # ==================================================

    def add_history(

        self,

        result

    ):

        if not hasattr(

            self,

            "history"

        ):

            self.history = []

        self.history.append(

            result

        )

    # ==================================================
    # Complete
    # ==================================================

    def complete_generation(

        self,

        result

    ):

        self.current_result = result

        self.preview_pipeline.update(

            result.content

        )

        self.preview_result(

            result

        )

        self.update_statistics(

            result

        )

        self.add_history(

            result

        )

        self.ai_ready()

        self.set_progress(

            1

        )

        self.set_status(

            "Generation Complete"

        )

    # ==================================================
    # Regenerate
    # ==================================================

    def regenerate(

        self

    ):

        if self.current_generator is None:

            return

        self.generate(

            self.current_generator

        )

    # ==================================================
    # Copy
    # ==================================================

    def copy_result(

        self

    ):

        if self.current_result is None:

            return

        self.clipboard_clear()

        self.clipboard_append(

            self.current_result.content

        )

    # ==================================================
    # Save Prompt
    # ==================================================

    def save_prompt(

        self

    ):

        self.saved_prompt = self.prompt_box.get(

            "1.0",

            "end"

        )

    # ==================================================
    # Restore Prompt
    # ==================================================

    def restore_prompt(

        self

    ):

        if not hasattr(

            self,

            "saved_prompt"

        ):

            return

        self.prompt_box.delete(

            "1.0",

            "end"

        )

        self.prompt_box.insert(

            "1.0",

            self.saved_prompt

        )

    # ==================================================
    # Export
    # ==================================================

    def export_result(

        self

    ):

        if self.current_result is None:

            self.set_status(

                "Nothing to export."

            )

            return

        exporters = {

            "PDF":

                "pdf",

            "DOCX":

                "docx",

            "Markdown":

                "md",

            "PowerPoint":

                "pptx",

            "Image":

                "png"

        }

        dialog = ctk.CTkInputDialog(

            text=(
                "Export Format\n\n"
                "PDF\n"
                "DOCX\n"
                "Markdown\n"
                "PowerPoint\n"
                "Image"
            ),

            title="Export"

        )

        choice = dialog.get_input()

        if choice is None:

            return

        choice = choice.strip()

        if choice not in exporters:

            self.set_status(

                "Unknown export format."

            )

            return

        extension = exporters[

            choice

        ]

        file = filedialog.asksaveasfilename(

            defaultextension=f".{extension}",

            filetypes=[

                (

                    f"{choice} File",

                    f"*.{extension}"

                )

            ]

        )

        if not file:

            return

        self.perform_export(

            choice,

            file

        )

    # ==================================================
    # Perform Export
    # ==================================================

    def perform_export(

        self,

        export_type,

        output_file

    ):

        try:

            self.ai_busy()

            self.set_status(

                "Exporting..."

            )

            self.set_progress(

                0.20

            )

            self.export_pipeline.export(

                export_type,

                self.current_result,

                output_file

            )

            self.set_progress(

                1

            )

            self.ai_ready()

            self.set_status(

                "Export Complete"

            )

        except Exception as error:

            self.show_error(

                error

            )

    # ==================================================
    # Quick Export
    # ==================================================

    def quick_export(

        self,

        export_type

    ):

        if self.current_result is None:

            return

        output = Path(

            "exports"

        )

        output.mkdir(

            exist_ok=True

        )

        filename = (

            self.current_result.title

            .replace(

                " ",

                "_"

            )

        )

        extension = {

            "PDF": "pdf",

            "DOCX": "docx",

            "Markdown": "md",

            "PowerPoint": "pptx",

            "Image": "png"

        }[

            export_type

        ]

        file = output / (

            filename +

            "." +

            extension

        )

        self.perform_export(

            export_type,

            str(

                file

            )

        )

    # ==================================================
    # Open Export Folder
    # ==================================================

    def open_export_folder(

        self

    ):

        folder = Path(

            "exports"

        )

        folder.mkdir(

            exist_ok=True

        )

        import os

        os.startfile(

            folder

        )

    # ==================================================
    # Copy Output
    # ==================================================

    def copy_output(

        self

    ):

        if self.current_result is None:

            return

        self.clipboard_clear()

        self.clipboard_append(

            self.current_result.content

        )

        self.set_status(

            "Copied to clipboard"

        )

    # ==================================================
    # Save As Markdown
    # ==================================================

    def save_markdown(

        self

    ):

        self.quick_export(

            "Markdown"

        )

    # ==================================================
    # Save As PDF
    # ==================================================

    def save_pdf(

        self

    ):

        self.quick_export(

            "PDF"

        )

    # ==================================================
    # Save As DOCX
    # ==================================================

    def save_docx(

        self

    ):

        self.quick_export(

            "DOCX"

        )

    # ==================================================
    # Save As PPT
    # ==================================================

    def save_presentation(

        self

    ):

        self.quick_export(

            "PowerPoint"

        )

    # ==================================================
    # Save As Image
    # ==================================================

    def save_image(

        self

    ):

        self.quick_export(

            "Image"

        )

    # ==================================================
    # Projects
    # ==================================================

    def new_project(

        self

    ):

        dialog = ctk.CTkInputDialog(

            title="New Project",

            text="Project Name"

        )

        name = dialog.get_input()

        if not name:

            return

        self.current_project = (

            self.project_manager.create(

                name=name,

                source=self.current_file

            )

        )

        self.set_project(

            name

        )

        self.set_results(

            0

        )

        self.set_status(

            "Project Created"

        )

    # ==================================================
    # Open Project
    # ==================================================

    def open_project(

        self

    ):

        file = filedialog.askopenfilename(

            title="Open Project",

            filetypes=[

                (

                    "WEBSTER Project",

                    "*.json"

                )

            ]

        )

        if not file:

            return

        self.current_project = (

            self.project_manager.load(

                file

            )

        )

        if self.current_project is None:

            return

        self.set_project(

            self.current_project.name

        )

        self.set_results(

            len(

                self.current_project.results

            )

        )

        self.set_status(

            "Project Loaded"

        )

    # ==================================================
    # Save Project
    # ==================================================

    def save_project(

        self

    ):

        if self.current_project is None:

            self.new_project()

            if self.current_project is None:

                return

        self.project_manager.save()

        self.set_status(

            "Project Saved"

        )

    # ==================================================
    # Save As
    # ==================================================

    def save_project_as(

        self

    ):

        if self.current_project is None:

            return

        dialog = ctk.CTkInputDialog(

            title="Save Project As",

            text="New Project Name"

        )

        name = dialog.get_input()

        if not name:

            return

        self.current_project.name = name

        self.project_manager.save()

        self.set_project(

            name

        )

    # ==================================================
    # Rename
    # ==================================================

    def rename_project(

        self

    ):

        if self.current_project is None:

            return

        dialog = ctk.CTkInputDialog(

            title="Rename Project",

            text="Project Name"

        )

        name = dialog.get_input()

        if not name:

            return

        self.current_project.name = name

        self.set_project(

            name

        )

    # ==================================================
    # Close
    # ==================================================

    def close_project(

        self

    ):

        self.current_project = None

        self.set_project(

            "Untitled"

        )

        self.set_results(

            0

        )

        self.set_status(

            "Project Closed"

        )

    # ==================================================
    # Autosave
    # ==================================================

    def autosave_project(

        self

    ):

        if self.current_project is None:

            return

        try:

            self.project_manager.save()

        except Exception:

            pass

        self.after(

            300000,

            self.autosave_project

        )

    # ==================================================
    # Recent
    # ==================================================

    def load_recent_projects(

        self

    ):

        self.recent_projects = (

            self.project_manager.list_projects()

        )

        return self.recent_projects

    # ==================================================
    # Restore Session
    # ==================================================

    def restore_last_session(

        self

    ):

        recent = self.load_recent_projects()

        if not recent:

            return

        try:

            self.current_project = (

                self.project_manager.load(

                    recent[0]

                )

            )

        except Exception:

            return

        if self.current_project:

            self.set_project(

                self.current_project.name

            )

            self.set_results(

                len(

                    self.current_project.results

                )

            )

    # ==================================================
    # Delete Project
    # ==================================================

    def delete_project(

        self,

        name

    ):

        self.project_manager.delete(

            name

        )

        self.set_status(

            "Project Deleted"

        )

    # ==================================================
    # Refresh
    # ==================================================

    def refresh_projects(

        self

    ):

        self.recent_projects = (

            self.project_manager.list_projects()

        )



    # ==================================================
    # Initialize
    # ==================================================

    def initialize(

        self

    ):

        self.restore_last_session()

        self.register_shortcuts()

        self.start_autosave()

        self.ai_ready()

        self.set_progress(

            0

        )

        self.set_status(

            "Study Hub Ready"

        )

    # ==================================================
    # Shortcuts
    # ==================================================

    def register_shortcuts(

        self

    ):

        shortcuts = {

            "<Control-o>":

                self.upload_document,

            "<Control-s>":

                self.save_project,

            "<Control-e>":

                self.export_result,

            "<Control-r>":

                self.regenerate,

            "<Control-n>":

                self.new_project,

            "<Control-l>":

                self.clear_workspace,

            "<Control-c>":

                self.copy_result

        }

        for key, callback in shortcuts.items():

            self.bind_all(

                key,

                lambda event,

                fn=callback:

                fn()

            )

    # ==================================================
    # Background Generation
    # ==================================================

    def generate_background(

        self,

        generator_name

    ):

        self.lock_ui()

        worker = threading.Thread(

            target=self._generation_worker,

            args=(

                generator_name,

            ),

            daemon=True

        )

        worker.start()

    # ==================================================
    # Worker
    # ==================================================

    def _generation_worker(

        self,

        generator_name

    ):

        try:

            self.after(

                0,

                lambda:

                self.ai_busy()

            )

            self.after(

                0,

                lambda:

                self.set_status(

                    "Generating..."

                )

            )

            self.generate(

                generator_name

            )

        finally:

            self.after(

                0,

                self.unlock_ui

            )

    # ==================================================
    # Autosave
    # ==================================================

    def start_autosave(

        self

    ):

        self.after(

            300000,

            self._autosave_loop

        )

    def _autosave_loop(

        self

    ):

        try:

            if self.current_project:

                self.project_manager.save()

        except Exception:

            pass

        self.after(

            300000,

            self._autosave_loop

        )

    # ==================================================
    # Lock
    # ==================================================

    def lock_ui(

        self

    ):

        for button in self.tool_buttons.values():

            button.configure(

                state="disabled"

            )

    # ==================================================
    # Unlock
    # ==================================================

    def unlock_ui(

        self

    ):

        for button in self.tool_buttons.values():

            button.configure(

                state="normal"

            )

    # ==================================================
    # Reset
    # ==================================================

    def reset_workspace(

        self

    ):

        self.clear_workspace()

        self.prompt_box.delete(

            "1.0",

            "end"

        )

        self.preview_box.configure(

            state="normal"

        )

        self.preview_box.delete(

            "1.0",

            "end"

        )

        self.preview_box.configure(

            state="disabled"

        )

        self.preview_tabs.set(

            "Output"

        )

        self.ai_ready()

        self.set_progress(

            0

        )

        self.set_status(

            "Workspace Reset"

        )

    # ==================================================
    # Refresh
    # ==================================================

    def refresh(

        self

    ):

        self.update_idletasks()

        self.update()

    # ==================================================
    # Lifecycle
    # ==================================================

    def on_show(

        self

    ):

        self.initialize()

    def on_hide(

        self

    ):

        if self.current_project:

            self.project_manager.save()

    # ==================================================
    # Shutdown
    # ==================================================

    def shutdown(

        self

    ):

        try:

            if self.current_project:

                self.project_manager.save()

        except Exception:

            pass

    # ==================================================
    # Destroy
    # ==================================================

    def destroy(

        self

    ):

        self.shutdown()

        super().destroy()

    # ==================================================
    # Diagnostics
    # ==================================================

    def diagnostics(

        self

    ):

        return {

            "project":

                None

                if self.current_project is None

                else self.current_project.name,

            "document":

                self.current_file,

            "generator":

                self.current_generator,

            "history":

                len(

                    getattr(

                        self,

                        "history",

                        []

                    )

                ),

            "results":

                0

                if self.current_project is None

                else len(

                    self.current_project.results

                ),

            "ai":

                self.ai_engine.__class__.__name__

        }