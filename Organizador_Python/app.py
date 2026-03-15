import os
import shutil
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime

# ─────────────────────────────────────────────
#  TIPOS SUPORTADOS
# ─────────────────────────────────────────────
CATEGORIAS = {
    "📸 Imagens":      [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".tif",
                        ".webp", ".heic", ".heif", ".svg", ".raw", ".cr2", ".nef",
                        ".arw", ".dng", ".psd", ".ai", ".eps"],
    "🎬 Vídeos":       [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm",
                        ".m4v", ".3gp", ".mpeg", ".mpg", ".ts", ".vob", ".ogv"],
    "🎵 Músicas":      [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a",
                        ".opus", ".aiff", ".mid", ".midi"],
    "📄 Documentos":   [".pdf", ".doc", ".docx", ".odt", ".rtf", ".txt", ".md",
                        ".tex", ".pages", ".wpd"],
    "📊 Planilhas":    [".xlsx", ".xls", ".csv", ".ods", ".tsv", ".numbers"],
    "📑 Apresentações":[".pptx", ".ppt", ".odp", ".key"],
    "🗜️ Compactados":  [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz",
                        ".iso", ".dmg", ".tar.gz", ".tar.bz2"],
    "💻 Código":       [".py", ".js", ".ts", ".html", ".css", ".java", ".c",
                        ".cpp", ".h", ".cs", ".go", ".rb", ".php", ".swift",
                        ".kt", ".rs", ".sh", ".bat", ".ps1", ".sql", ".json",
                        ".xml", ".yaml", ".yml", ".toml", ".ini", ".env"],
    "🗄️ Bancos de Dados":[".db", ".sqlite", ".sqlite3", ".mdb", ".accdb", ".dbf"],
    "🖋️ Fontes":       [".ttf", ".otf", ".woff", ".woff2", ".eot"],
    "🔧 Executáveis":  [".exe", ".msi", ".apk", ".app", ".deb", ".rpm", ".bin",
                        ".run", ".appimage"],
    "🌐 Web":          [".html", ".htm", ".xhtml", ".css", ".js", ".ts",
                        ".jsx", ".tsx", ".php", ".asp", ".aspx"],
    "🗺️ Atalhos/Links":[".lnk", ".url", ".desktop", ".webloc"],
    "🎨 Ícones":       [".ico", ".icns", ".cur"],
    "📦 Backups":      [".bak", ".bkp", ".backup", ".old", ".orig", ".temp", ".tmp"],
    "📧 E-mails":      [".eml", ".msg", ".pst", ".ost", ".mbox"],
    "📋 Configurações":[".cfg", ".conf", ".ini", ".reg", ".plist", ".log"],
    "🖨️ 3D / CAD":     [".stl", ".obj", ".fbx", ".blend", ".3ds", ".dae",
                        ".gltf", ".glb", ".dwg", ".dxf"],
    "🔑 Certificados": [".pem", ".crt", ".cer", ".p12", ".pfx", ".key", ".pub"],
    "📰 eBooks":        [".epub", ".mobi", ".azw", ".azw3", ".fb2", ".djvu"],
}

NOMES_PASTAS = {
    "📸 Imagens":       "Imagens",
    "🎬 Vídeos":        "Videos",
    "🎵 Músicas":       "Musicas",
    "📄 Documentos":    "Documentos",
    "📊 Planilhas":     "Planilhas",
    "📑 Apresentações": "Apresentacoes",
    "🗜️ Compactados":   "Compactados",
    "💻 Código":        "Codigo",
    "🗄️ Bancos de Dados":"Bancos_de_Dados",
    "🖋️ Fontes":        "Fontes",
    "🔧 Executáveis":   "Executaveis",
    "🌐 Web":           "Web",
    "🗺️ Atalhos/Links": "Atalhos",
    "🎨 Ícones":        "Icones",
    "📦 Backups":       "Backups",
    "📧 E-mails":       "Emails",
    "📋 Configurações": "Configuracoes",
    "🖨️ 3D / CAD":      "3D_CAD",
    "🔑 Certificados":  "Certificados",
    "📰 eBooks":         "eBooks",
}

# ─────────────────────────────────────────────
#  LÓGICA DE ORGANIZAÇÃO
# ─────────────────────────────────────────────
def construir_mapa(categorias_selecionadas):
    mapa = {}
    for cat in categorias_selecionadas:
        for ext in CATEGORIAS.get(cat, []):
            mapa[ext.lower()] = cat
    return mapa


def organizar(caminho, categorias_selecionadas, modo_copia, callback_log, callback_fim):
    mapa = construir_mapa(categorias_selecionadas)
    movidos = 0
    erros = 0
    ignorados = 0

    try:
        arquivos = [
            f for f in os.listdir(caminho)
            if os.path.isfile(os.path.join(caminho, f))
        ]
    except Exception as e:
        callback_log(f"[ERRO] Não foi possível listar a pasta: {e}", "erro")
        callback_fim(0, 1, 0)
        return

    callback_log(f"[INFO] {len(arquivos)} arquivo(s) encontrado(s).", "info")

    for arquivo in arquivos:
        _, ext = os.path.splitext(arquivo)
        ext = ext.lower()
        cat = mapa.get(ext)

        if cat is None:
            callback_log(f"[IGNORADO] {arquivo} (extensão não mapeada: {ext or 'sem extensão'})", "aviso")
            ignorados += 1
            continue

        pasta_destino = os.path.join(caminho, NOMES_PASTAS[cat])
        os.makedirs(pasta_destino, exist_ok=True)

        origem = os.path.join(caminho, arquivo)
        destino = os.path.join(pasta_destino, arquivo)

        # Evitar sobrescrever
        if os.path.exists(destino):
            base, suf = os.path.splitext(arquivo)
            ts = datetime.now().strftime("%Y%m%d%H%M%S")
            destino = os.path.join(pasta_destino, f"{base}_{ts}{suf}")

        try:
            if modo_copia:
                shutil.copy2(origem, destino)
                acao = "COPIADO"
            else:
                shutil.move(origem, destino)
                acao = "MOVIDO"
            callback_log(f"[{acao}] {arquivo} → {NOMES_PASTAS[cat]}/", "ok")
            movidos += 1
        except Exception as e:
            callback_log(f"[ERRO] {arquivo}: {e}", "erro")
            erros += 1

    callback_fim(movidos, erros, ignorados)


# ─────────────────────────────────────────────
#  INTERFACE GRÁFICA
# ─────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Organizador de Arquivos")
        self.geometry("860x680")
        self.minsize(720, 540)
        self.configure(bg="#0f1117")
        self.resizable(True, True)

        self._setup_styles()
        self._build_ui()

    # ── Estilos ──────────────────────────────
    def _setup_styles(self):
        self.CORES = {
            "bg":        "#0f1117",
            "surface":   "#1a1d27",
            "border":    "#2a2d3e",
            "accent":    "#6c63ff",
            "accent2":   "#a78bfa",
            "texto":     "#e2e8f0",
            "subtexto":  "#94a3b8",
            "ok":        "#34d399",
            "aviso":     "#fbbf24",
            "erro":      "#f87171",
            "info":      "#60a5fa",
        }

        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TFrame",    background=self.CORES["bg"])
        style.configure("Card.TFrame", background=self.CORES["surface"],
                        relief="flat")

        style.configure("TLabel",
                        background=self.CORES["bg"],
                        foreground=self.CORES["texto"],
                        font=("Segoe UI", 10))
        style.configure("Title.TLabel",
                        background=self.CORES["bg"],
                        foreground=self.CORES["texto"],
                        font=("Segoe UI", 18, "bold"))
        style.configure("Sub.TLabel",
                        background=self.CORES["bg"],
                        foreground=self.CORES["subtexto"],
                        font=("Segoe UI", 9))
        style.configure("Card.TLabel",
                        background=self.CORES["surface"],
                        foreground=self.CORES["texto"],
                        font=("Segoe UI", 10))
        style.configure("CardSub.TLabel",
                        background=self.CORES["surface"],
                        foreground=self.CORES["subtexto"],
                        font=("Segoe UI", 9))

        style.configure("Accent.TButton",
                        background=self.CORES["accent"],
                        foreground="white",
                        font=("Segoe UI", 10, "bold"),
                        padding=(16, 8),
                        relief="flat", borderwidth=0)
        style.map("Accent.TButton",
                  background=[("active", self.CORES["accent2"]),
                               ("pressed", "#5b52e8")])

        style.configure("Ghost.TButton",
                        background=self.CORES["surface"],
                        foreground=self.CORES["subtexto"],
                        font=("Segoe UI", 9),
                        padding=(10, 6),
                        relief="flat", borderwidth=0)
        style.map("Ghost.TButton",
                  background=[("active", self.CORES["border"])],
                  foreground=[("active", self.CORES["texto"])])

        style.configure("TCheckbutton",
                        background=self.CORES["surface"],
                        foreground=self.CORES["texto"],
                        font=("Segoe UI", 9))
        style.map("TCheckbutton",
                  background=[("active", self.CORES["surface"])],
                  foreground=[("active", self.CORES["accent2"])])

        style.configure("TScrollbar",
                        background=self.CORES["border"],
                        troughcolor=self.CORES["surface"],
                        arrowcolor=self.CORES["subtexto"],
                        borderwidth=0)

        style.configure("Horizontal.TProgressbar",
                        troughcolor=self.CORES["border"],
                        background=self.CORES["accent"],
                        borderwidth=0, thickness=6)

    # ── UI principal ─────────────────────────
    def _build_ui(self):
        C = self.CORES

        # ── Header
        hdr = ttk.Frame(self)
        hdr.pack(fill="x", padx=24, pady=(20, 4))
        ttk.Label(hdr, text="📂  Organizador de Arquivos", style="Title.TLabel").pack(side="left")
        ttk.Label(hdr, text="v2.0", style="Sub.TLabel").pack(side="left", padx=(8, 0), pady=(6, 0))

        # ── Card: Pasta
        pasta_card = self._card(self, pady_top=12)
        ttk.Label(pasta_card, text="PASTA ALVO", style="CardSub.TLabel").pack(anchor="w")

        row_pasta = ttk.Frame(pasta_card, style="Card.TFrame")
        row_pasta.pack(fill="x", pady=(4, 0))

        self.var_pasta = tk.StringVar()
        entry_pasta = tk.Entry(row_pasta,
                               textvariable=self.var_pasta,
                               bg=C["border"], fg=C["texto"],
                               insertbackground=C["texto"],
                               relief="flat", font=("Segoe UI", 10),
                               highlightthickness=1,
                               highlightbackground=C["border"],
                               highlightcolor=C["accent"])
        entry_pasta.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 8))

        ttk.Button(row_pasta, text="Procurar…",
                   style="Ghost.TButton",
                   command=self._selecionar_pasta).pack(side="left")

        # ── Card: Categorias
        cat_card = self._card(self, pady_top=10)
        row_cat_hdr = ttk.Frame(cat_card, style="Card.TFrame")
        row_cat_hdr.pack(fill="x", pady=(0, 8))
        ttk.Label(row_cat_hdr, text="CATEGORIAS", style="CardSub.TLabel").pack(side="left")

        btn_todos = ttk.Button(row_cat_hdr, text="Marcar todos",
                               style="Ghost.TButton",
                               command=lambda: self._marcar_todos(True))
        btn_todos.pack(side="right", padx=(4, 0))
        btn_nenhum = ttk.Button(row_cat_hdr, text="Desmarcar todos",
                                style="Ghost.TButton",
                                command=lambda: self._marcar_todos(False))
        btn_nenhum.pack(side="right")

        # Grid de checkboxes
        grid = ttk.Frame(cat_card, style="Card.TFrame")
        grid.pack(fill="x")
        self.vars_cat = {}
        cats = list(CATEGORIAS.keys())
        cols = 3
        for i, cat in enumerate(cats):
            var = tk.BooleanVar(value=True)
            self.vars_cat[cat] = var
            cb = ttk.Checkbutton(grid, text=cat, variable=var)
            cb.grid(row=i // cols, column=i % cols,
                    sticky="w", padx=(0, 16), pady=2)

        # ── Card: Opções
        opt_card = self._card(self, pady_top=10)
        ttk.Label(opt_card, text="OPÇÕES", style="CardSub.TLabel").pack(anchor="w", pady=(0, 6))

        opt_row = ttk.Frame(opt_card, style="Card.TFrame")
        opt_row.pack(fill="x")

        self.var_copia = tk.BooleanVar(value=False)
        ttk.Checkbutton(opt_row, text="Copiar (manter originais)",
                        variable=self.var_copia).pack(side="left", padx=(0, 24))

        self.var_subpastas = tk.BooleanVar(value=False)
        ttk.Checkbutton(opt_row, text="Incluir subpastas (recursivo)",
                        variable=self.var_subpastas).pack(side="left")

        # ── Botão executar
        btn_row = ttk.Frame(self)
        btn_row.pack(fill="x", padx=24, pady=(12, 0))
        self.btn_exec = ttk.Button(btn_row, text="▶  Organizar Agora",
                                   style="Accent.TButton",
                                   command=self._executar)
        self.btn_exec.pack(side="right")

        ttk.Button(btn_row, text="🗑  Limpar log",
                   style="Ghost.TButton",
                   command=self._limpar_log).pack(side="right", padx=(0, 8))

        # ── Progress bar
        self.progress = ttk.Progressbar(self, mode="indeterminate",
                                        style="Horizontal.TProgressbar")
        self.progress.pack(fill="x", padx=24, pady=(10, 0))

        # ── Log
        log_card = self._card(self, pady_top=10, expand=True)
        ttk.Label(log_card, text="LOG DE OPERAÇÕES", style="CardSub.TLabel").pack(anchor="w", pady=(0, 6))

        log_frame = ttk.Frame(log_card, style="Card.TFrame")
        log_frame.pack(fill="both", expand=True)

        self.log_text = tk.Text(log_frame,
                                bg=C["bg"], fg=C["texto"],
                                font=("Consolas", 9),
                                relief="flat", state="disabled",
                                wrap="word",
                                insertbackground=C["texto"],
                                selectbackground=C["accent"])
        sb = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.log_text.pack(side="left", fill="both", expand=True)

        # Tags de cor no log
        self.log_text.tag_config("ok",    foreground=C["ok"])
        self.log_text.tag_config("erro",  foreground=C["erro"])
        self.log_text.tag_config("aviso", foreground=C["aviso"])
        self.log_text.tag_config("info",  foreground=C["info"])
        self.log_text.tag_config("fim",   foreground=C["accent2"],
                                  font=("Consolas", 9, "bold"))

        # ── Status bar
        self.var_status = tk.StringVar(value="Pronto.")
        status_bar = tk.Label(self, textvariable=self.var_status,
                              bg=C["border"], fg=C["subtexto"],
                              font=("Segoe UI", 8),
                              anchor="w", padx=12, pady=4)
        status_bar.pack(fill="x", side="bottom")

    def _card(self, parent, pady_top=0, expand=False):
        C = self.CORES
        outer = ttk.Frame(parent)
        outer.pack(fill="both" if expand else "x",
                   expand=expand, padx=24, pady=(pady_top, 0))
        inner = tk.Frame(outer, bg=C["surface"],
                         highlightthickness=1,
                         highlightbackground=C["border"])
        inner.pack(fill="both", expand=expand)
        pad = ttk.Frame(inner, style="Card.TFrame")
        pad.pack(fill="both", expand=expand, padx=16, pady=12)
        return pad

    # ── Ações ─────────────────────────────────
    def _selecionar_pasta(self):
        caminho = filedialog.askdirectory(title="Selecione a pasta para organizar")
        if caminho:
            self.var_pasta.set(caminho)

    def _marcar_todos(self, valor: bool):
        for var in self.vars_cat.values():
            var.set(valor)

    def _limpar_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

    def _log(self, mensagem: str, tag: str = ""):
        self.log_text.configure(state="normal")
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{ts}] {mensagem}\n", tag)
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _executar(self):
        caminho = self.var_pasta.get().strip()
        if not caminho or not os.path.isdir(caminho):
            messagebox.showerror("Pasta inválida",
                                 "Selecione uma pasta válida antes de continuar.")
            return

        selecionadas = [cat for cat, var in self.vars_cat.items() if var.get()]
        if not selecionadas:
            messagebox.showwarning("Nenhuma categoria",
                                   "Selecione ao menos uma categoria para organizar.")
            return

        self.btn_exec.configure(state="disabled")
        self.progress.start(12)
        self.var_status.set("Organizando…")
        self._log(f"Iniciando organização em: {caminho}", "info")
        self._log(f"Categorias ativas: {len(selecionadas)}", "info")

        def worker():
            organizar(
                caminho,
                selecionadas,
                self.var_copia.get(),
                callback_log=lambda m, t: self.after(0, self._log, m, t),
                callback_fim=lambda mv, er, ig: self.after(0, self._finalizar, mv, er, ig),
            )

        threading.Thread(target=worker, daemon=True).start()

    def _finalizar(self, movidos, erros, ignorados):
        self.progress.stop()
        self.btn_exec.configure(state="normal")
        resumo = (f"✅ Concluído — "
                  f"{movidos} movido(s) | {erros} erro(s) | {ignorados} ignorado(s)")
        self._log(resumo, "fim")
        self.var_status.set(resumo)
        if erros == 0:
            messagebox.showinfo("Pronto!", resumo)
        else:
            messagebox.showwarning("Concluído com avisos", resumo)


# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()