class Palette:
    BG = (12, 14, 26)
    GRID = (28, 32, 52)
    WHITE = (220, 226, 240)

    # Cores de interface
    CYAN = (90, 205, 220)
    MAGENTA = (210, 110, 190)
    YELLOW = (225, 200, 100)
    GREEN = (125, 200, 135)
    ORANGE = (225, 155, 100)
    PINK = (220, 140, 175)
    LBLUE = (115, 165, 220)
    RED = (220, 110, 115)

    # Cores por linguagem.
    # Paleta com saturação moderada e brilho semelhante.
    LANG: dict[str, tuple[int, int, int]] = {
        # Linguagens de propósito geral
        "Python":       (115, 185, 155),
        "JavaScript":   (220, 195, 105),
        "TypeScript":   (100, 155, 215),
        "Java":         (210, 125, 115),
        "C":            (130, 155, 205),
        "C++":          (190, 125, 140),
        "C#":           (145, 145, 215),
        "F#":           (160, 135, 205),
        "Go":           (95, 190, 205),
        "Rust":         (205, 145, 115),
        "Ruby":         (205, 120, 130),
        "PHP":          (155, 145, 205),
        "Perl":         (130, 165, 200),
        "R":            (110, 160, 215),
        "Dart":         (100, 185, 205),
        "Kotlin":       (190, 135, 200),
        "Swift":        (220, 150, 110),
        "Objective-C":  (155, 165, 190),
        "Scala":        (200, 125, 125),
        "Groovy":       (175, 170, 115),
        "Lua":          (125, 145, 205),
        "Haskell":      (165, 145, 195),
        "Elixir":       (175, 130, 195),
        "Erlang":       (195, 135, 155),
        "Clojure":      (135, 180, 135),
        "OCaml":        (220, 155, 110),
        "Julia":        (180, 135, 180),
        "Zig":          (210, 165, 110),
        "Nim":          (195, 175, 115),
        "Fortran":      (130, 155, 195),
        "COBOL":        (150, 175, 195),
        "Assembly":     (170, 155, 175),
        "Prolog":       (185, 135, 155),
        "Ada":          (140, 155, 205),
        "Pascal":       (125, 170, 195),
        "Delphi":       (120, 175, 180),
        "V":            (145, 185, 155),
        "Crystal":      (155, 175, 185),
        "Solidity":     (155, 155, 175),

        # Shell e automação
        "Shell":        (120, 195, 175),
        "Bash":         (120, 195, 175),
        "Zsh":          (110, 185, 170),
        "Fish":         (105, 180, 190),
        "PowerShell":   (105, 155, 220),
        "Batch":        (160, 170, 150),
        "Makefile":     (190, 175, 120),
        "Just":         (180, 165, 130),
        "AWK":          (150, 175, 155),
        "Sed":          (155, 180, 160),

        # Web
        "HTML":         (220, 150, 110),
        "XML":          (205, 145, 165),
        "CSS":          (115, 165, 215),
        "SCSS":         (200, 140, 175),
        "Sass":         (195, 135, 170),
        "Less":         (135, 155, 210),
        "Vue":          (110, 185, 155),
        "Svelte":       (215, 140, 110),
        "Astro":        (190, 145, 175),
        "JSX":          (125, 175, 205),
        "TSX":          (110, 160, 210),
        "WebAssembly":  (145, 150, 210),
        "GraphQL":      (200, 130, 185),

        # Dados e consultas
        "SQL":          (125, 170, 210),
        "PL/SQL":       (145, 165, 200),
        "T-SQL":        (135, 160, 205),
        "HiveQL":       (195, 180, 110),
        "Sparql":       (155, 170, 200),
        "Cypher":       (115, 180, 175),
        "Pig":          (185, 165, 120),
        "R":            (110, 160, 215),
        "MATLAB":       (200, 160, 115),
        "Wolfram":      (205, 155, 125),

        # Ciência de dados e notebooks
        "Jupyter":      (210, 145, 115),
        "Julia":        (180, 135, 180),
        "SAS":          (125, 165, 200),
        "Stata":        (135, 180, 175),
        "SPSS":         (150, 175, 195),

        # Infraestrutura e configuração
        "Dockerfile":   (105, 160, 215),
        "Docker":       (105, 160, 215),
        "YAML":         (185, 155, 195),
        "JSON":         (195, 180, 120),
        "TOML":         (180, 160, 130),
        "INI":          (175, 165, 140),
        "Nginx":        (125, 185, 145),
        "Terraform":    (145, 140, 210),
        "HCL":          (145, 140, 210),
        "Nix":          (130, 170, 200),
        "Ansible":      (195, 125, 135),
        "Puppet":       (185, 140, 150),
        "Chef":         (200, 150, 115),
        "Vagrant":      (135, 165, 200),
        "Kubernetes":   (115, 150, 215),

        # Documentação e marcação
        "Markdown":     (165, 175, 190),
        "MDX":          (155, 165, 205),
        "LaTeX":        (125, 175, 155),
        " reStructuredText": (165, 175, 185),
        "AsciiDoc":     (175, 170, 155),

        # Sistemas de build e dependências
        "CMake":        (135, 160, 195),
        "Meson":        (145, 175, 155),
        "Gradle":       (125, 175, 160),
        "Maven":        (185, 145, 135),
        "Bazel":        (180, 155, 125),

        # Outros formatos e linguagens
        "Protocol Buffers": (135, 165, 195),
        "Protobuf":     (135, 165, 195),
        "Thrift":       (150, 165, 185),
        "Avro":         (175, 155, 190),
        "Rego":         (145, 175, 155),
        "Vimscript":    (130, 185, 150),
        "Emacs Lisp":   (175, 145, 190),
        "Lisp":         (175, 145, 190),
        "Scheme":       (185, 150, 175),
        "Racket":       (190, 145, 170),
        "Solidity":     (155, 155, 175),
        "GLSL":         (135, 165, 205),
        "HLSL":         (145, 170, 195),
        "ShaderLab":    (155, 165, 200),
        "GDScript":     (115, 170, 195),
        "Godot":        (115, 170, 195),
        "Ren'Py":       (195, 145, 170),
        "Verilog":      (155, 160, 195),
        "SystemVerilog": (155, 160, 195),
        "VHDL":         (165, 155, 195),
        "Solidity":     (155, 155, 175),
        "QML":          (120, 180, 170),
        "CoffeeScript": (155, 170, 190),
        "Elm":          (125, 170, 205),
        "PureScript":   (145, 155, 210),
        "Reason":       (175, 145, 195),
        "ReScript":     (145, 155, 205),
        "EJS":          (185, 165, 120),
        "Handlebars":   (195, 155, 115),
        "Mustache":     (185, 155, 125),
        "Jinja":        (135, 180, 145),
        "Liquid":       (135, 175, 155),
        "Twig":         (140, 175, 145),
        "SQLAlchemy":   (145, 165, 190),
    }

    # Ciclo de fallback ordenado por matiz.
    # Cores menos agressivas que os neons originais.
    DEFAULT_CYCLE = [
        (115, 185, 155),  # verde
        (95, 190, 205),   # ciano
        (105, 155, 215),  # azul
        (155, 145, 210),  # violeta
        (195, 140, 185),  # magenta
        (215, 140, 145),  # vermelho
        (220, 155, 110),  # laranja
        (220, 195, 105),  # amarelo
    ]

    @classmethod
    def for_lang(cls, lang: str, index: int = 0) -> tuple[int, int, int]:
        # Busca exata primeiro; fallback sem diferenciar maiúsculas.
        color = cls.LANG.get(lang)
        if color is not None:
            return color

        normalized = lang.strip().casefold()
        for name, color in cls.LANG.items():
            if name.casefold() == normalized:
                return color

        return cls.DEFAULT_CYCLE[index % len(cls.DEFAULT_CYCLE)]
