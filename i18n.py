"""Textos de la interfaz en español."""

from __future__ import annotations

from typing import Any

STRINGS: dict[str, str] = {
    "page_title": "Inversiones (MAF) - Universidad EAFIT",
    "title": "Inversiones (MAF) - Universidad EAFIT",
    "market_data": "Datos de mercado",
    "ticker": "Símbolo",
    "search_symbol": "Buscar símbolo",
    "search_placeholder": "p. ej. AAPL — reemplaza la selección de arriba",
    "start": "Inicio",
    "end": "Fin",
    "indicators": "Indicadores",
    "load_refresh": "Cargar / actualizar",
    "enter_ticker": "Ingresa un símbolo bursátil.",
    "start_before_end": "La fecha de inicio debe ser anterior a la de fin.",
    "downloading": "Descargando {ticker}…",
    "indicator_hits": "Apariciones del indicador",
    "sma_cross_hits": "Cruce de medias (SMA)",
    "hits_caption": (
        "Cada número indica en cuántos **días bursátiles** de tu rango apareció esa señal. "
        "Son pistas, no consejo de compra o venta."
    ),
    "raw_data": "Datos en bruto (últimas 10 filas)",
    "considerations": "Consideraciones (ejercicio académico)",
    "tab_dashboard": "Análisis",
    "tab_fibonacci": "Fibonacci",
    "tab_tickers": "Símbolos",
    "tab_considerations": "Consideraciones",
    "tab_members": "Integrantes",
    "members_title": "Integrantes del proyecto",
    "members_intro": "Equipo del ejercicio académico de inversiones — Universidad EAFIT.",
    "tickers_intro": (
        "Símbolos incluidos en el ejercicio, agrupados por lista. "
        "Puedes analizarlos en la pestaña **Análisis**."
    ),
    "tickers_owner_label": "Lista: {owner}",
    "load_data_prompt": (
        "Elige un símbolo y fechas en la barra lateral, luego pulsa **Cargar / actualizar**."
    ),
    "ticker_summary": "Qué está pasando con {ticker}",
    "summary_disclaimer": (
        "Lectura sencilla del gráfico y los patrones—no es consejo de compra o venta."
    ),
    "summary_intro": (
        "Lectura sencilla de **{ticker}** con precios diarios del **{start}** al **{end}**."
    ),
    "summary_trend_up": (
        "El último cierre (**{close:.2f}**) está **por encima** de las medias de 20 y 50 días. "
        "Eso suele indicar una tendencia **alcista** reciente."
    ),
    "summary_trend_down": (
        "El último cierre (**{close:.2f}**) está **por debajo** de las medias de 20 y 50 días. "
        "Eso suele indicar una tendencia **bajista** reciente."
    ),
    "summary_trend_mixed": (
        "El último cierre (**{close:.2f}**) queda **entre** las medias (20 días: {sma20:.2f}, "
        "50 días: {sma50:.2f}). La tendencia se ve **mixta o lateral**."
    ),
    "summary_trend_short": "En los últimos ~20 días bursátiles, el precio se movió cerca de **{pct:+.1f}%**.",
    "summary_trend_unknown": (
        "Aún no hay suficientes días para comparar el precio con las medias de 20 y 50 días."
    ),
    "summary_recent_title": "**Últimos ~20 días bursátiles — patrones detectados:**",
    "summary_recent_item": "- {label}: {count} día(s)",
    "summary_recent_none": (
        "En los **últimos ~20 días bursátiles** no se detectó ninguno de los patrones de abajo."
    ),
    "summary_overall_title": "**Todo el periodo — balance de patrones:**",
    "summary_overall_bullish": (
        "Señales que suelen inclinarse **alcistas** (martillo, martillo invertido, envolvente alcista): "
        "**{count}** día(s) en total."
    ),
    "summary_overall_bearish": (
        "Señales que suelen inclinarse **bajistas** (estrella fugaz, envolvente bajista): "
        "**{count}** día(s) en total."
    ),
    "summary_overall_neutral": (
        "Señales que suelen indicar **pausa o indecisión** (estrella doji, harami): "
        "**{count}** día(s) en total."
    ),
    "summary_overall_none": "No se detectaron patrones de velas en este rango de fechas.",
    "summary_overall_read_bullish": (
        "En conjunto, los patrones **alcistas** aparecieron más que los bajistas."
    ),
    "summary_overall_read_bearish": (
        "En conjunto, los patrones **bajistas** aparecieron más que los alcistas."
    ),
    "summary_overall_read_balanced": (
        "En conjunto, patrones alcistas y bajistas aparecieron un número **parecido** de veces."
    ),
    "summary_overall_read_neutral_heavy": (
        "Hubo muchos días con patrones de **pausa / indecisión** más que señales claras arriba o abajo."
    ),
    "summary_sma_position_above": (
        "Hoy la **media de 20 días está por encima de la de 50 días**. "
        "Muchos la leen como **impulso alcista**."
    ),
    "summary_sma_position_below": (
        "Hoy la **media de 20 días está por debajo de la de 50 días**. "
        "Muchos la leen como **impulso más débil**."
    ),
    "summary_sma_position_equal": (
        "Hoy las medias de 20 y 50 días están **muy cerca**—la tendencia no está clara."
    ),
    "summary_sma_cross_period": (
        "**Cruces de medias** en el periodo: **{bull}** alcista(s) (la de 20 cruzó **arriba** "
        "de la de 50) y **{bear}** bajista(s) (cruzó **abajo**)."
    ),
    "summary_sma_cross_none": (
        "No hubo cruces de medias en este rango (la media corta no cambió de lado respecto a la larga)."
    ),
    "summary_sma_cross_last_bull": "Último cruce **alcista**: **{date}**.",
    "summary_sma_cross_last_bear": "Último cruce **bajista**: **{date}**.",
    "summary_sma_cross_recent": (
        "En los **últimos ~20 días bursátiles**: **{bull}** cruce(s) alcista(s) y "
        "**{bear}** bajista(s)."
    ),
    "error_no_data": "No hay datos para {ticker!r} en el rango de fechas seleccionado.",
    "error_missing_columns": "Faltan columnas en la descarga: {columns}",
    "fib_title": "Extensión de Fibonacci",
    "fib_intro": (
        "Elige **tres fechas en orden cronológico** para definir el tramo A→B→C. "
        "**A** marca el inicio del impulso, **B** el fin del impulso y **C** el fin "
        "del retroceso. Los niveles se calculan con **C + ratio × (B − A)**."
    ),
    "fib_point_a": "Punto A (inicio del impulso)",
    "fib_point_b": "Punto B (fin del impulso)",
    "fib_point_c": "Punto C (fin del retroceso)",
    "fib_date": "Fecha",
    "fib_price_field": "Precio del punto",
    "fib_price_close": "Cierre",
    "fib_price_high": "Máximo",
    "fib_price_low": "Mínimo",
    "fib_calculate": "Calcular niveles",
    "fib_load_data_prompt": (
        "Carga datos en la barra lateral antes de calcular la extensión de Fibonacci."
    ),
    "fib_error_distinct": "A, B y C deben ser **fechas distintas**.",
    "fib_error_order": "Las fechas deben ir en orden: **A antes de B antes de C**.",
    "fib_levels_title": "Niveles calculados",
    "fib_levels_caption": "Impulso (B − A): **{impulse:.2f}** · Precio en C: **{price_c:.2f}**",
    "fib_date_option": "{date} — {column}: {price:.2f}",
    "fib_level_label": "Fib {ratio}",
    "fib_swing_legend": "Tramo A→B→C",
    "fib_ratio": "Ratio",
    "fib_level": "Nivel",
}

CONSIDERATIONS = """
**Propósito.** Esta aplicación es un ejercicio universitario para explorar patrones de
velas diarios y medias móviles simples. Sirve solo para aprendizaje y visualización—no
constituye asesoría financiera ni recomendación de inversión.

**Fuente de datos.** Los precios se descargan de [Yahoo Finance](https://finance.yahoo.com/)
mediante la biblioteca [yfinance](https://github.com/ranaroussi/yfinance). Se usan barras
**diarias** (apertura, máximo, mínimo, cierre, volumen) para el símbolo y el rango de
fechas elegidos. Los datos de Yahoo pueden llegar con retraso, revisiones o huecos; los
desdoblamientos y dividendos pueden alterar series históricas según cómo Yahoo las reporte.

**Construcción.** El flujo está implementado en **Python**: **Streamlit** para el panel
interactivo, **TA-Lib** para detectar patrones de velas, **Plotly** para los gráficos y
**pandas** para manipular los datos.

**Metodología y límites.**

- Las señales provienen de funciones basadas en reglas de TA-Lib, no de un modelo predictivo entrenado.
- Los conteos indican cuántas veces apareció un patrón en la ventana elegida; no son rentabilidades
  backtesteadas y no incluyen comisiones, impuestos ni deslizamiento.
- Los patrones técnicos son señales interpretativas; la frecuencia pasada no predice precios futuros.
- Los resultados dependen del símbolo, el calendario y los feriados bursátiles (es normal faltar barras).

**Referencias**

1. Yahoo Finance. *Portal de datos de mercado.* https://finance.yahoo.com/
2. Roussi, A. *yfinance: descargador de datos de Yahoo! Finance.* https://github.com/ranaroussi/yfinance
3. Streamlit Inc. *Streamlit: forma rápida de crear apps de datos.* https://streamlit.io/
4. TA-Lib Group. *TA-Lib: biblioteca de análisis técnico.* https://ta-lib.org/
5. Plotly Technologies Inc. *Plotly: interfaz para ciencia de datos.* https://plotly.com/python/
6. Equipo de desarrollo de pandas. *pandas: análisis de datos en Python.* https://pandas.pydata.org/
7. Python Software Foundation. *Lenguaje de programación Python.* https://www.python.org/
""".strip()

PATTERNS: dict[str, dict[str, str]] = {
    "doji_star": {
        "label": "Estrella Doji",
        "description": (
            "Apertura y cierre casi iguales tras un hueco. "
            "Suele indicar que la tendencia se frena o puede girar."
        ),
    },
    "harami": {
        "label": "Harami",
        "description": (
            "Un día pequeño queda dentro del rango del día anterior. "
            "Suele indicar que el impulso se está debilitando."
        ),
    },
    "hammer": {
        "label": "Martillo",
        "description": (
            "Cuerpo pequeño arriba con mecha inferior larga. "
            "Tras una caída, puede indicar que entran compradores."
        ),
    },
    "inverted_hammer": {
        "label": "Martillo invertido",
        "description": (
            "Cuerpo pequeño abajo con mecha superior larga. "
            "Tras una caída, puede indicar que la presión vendedora afloja."
        ),
    },
    "shooting_star": {
        "label": "Estrella fugaz",
        "description": (
            "Cuerpo pequeño abajo con mecha superior larga tras una subida. "
            "Puede indicar que los vendedores reaccionan."
        ),
    },
    "bullish_engulfing": {
        "label": "Envolvente alcista",
        "description": (
            "Un día verde cubre por completo el día rojo anterior. "
            "Suele leerse como control de los compradores."
        ),
    },
    "bearish_engulfing": {
        "label": "Envolvente bajista",
        "description": (
            "Un día rojo cubre por completo el día verde anterior. "
            "Suele leerse como control de los vendedores."
        ),
    },
}

CHART: dict[str, str] = {
    "sma20": "MM 20",
    "sma50": "MM 50",
    "volume": "Volumen",
    "sma_cross_bull": "MM 20 cruza arriba de MM 50",
    "sma_cross_bear": "MM 20 cruza abajo de MM 50",
}

MEMBERS: list[dict[str, str]] = [
    {
        "name": "Juan Esteban Palacio Salazar",
        "email": "jepalacis1@eafit.edu.co",
    },
    {
        "name": "Duvan Cardona Gutierrez",
        "email": "dcardonag@eafit.edu.co",
    },
]

TICKER_GROUPS: dict[str, list[str]] = {
    "Juanes": ["JNJ", "MCD", "CIB", "JPM", "SPY"],
    "Duvan": ["NBIS", "RKLB", "IYW", "AAPL", "DAL"],
}

TICKER_CATALOG: dict[str, dict[str, str]] = {
    "JNJ": {
        "name": "Johnson & Johnson",
        "description": (
            "Compañía global de salud: medicamentos, dispositivos médicos "
            "y productos de cuidado personal."
        ),
    },
    "MCD": {
        "name": "McDonald's",
        "description": (
            "Cadena internacional de comida rápida; sus acciones suelen "
            "asociarse a consumo masivo y franquicias."
        ),
    },
    "CIB": {
        "name": "Grupo Cibest S.A.",
        "description": (
            "Holding financiero colombiano (Bancolombia); agrupa negocios "
            "de banca, corretaje e inversiones en el país."
        ),
    },
    "JPM": {
        "name": "JPMorgan Chase & Co.",
        "description": (
            "Uno de los mayores bancos de Estados Unidos; expuesto a "
            "crédito, mercados de capital y banca de inversión."
        ),
    },
    "SPY": {
        "name": "SPDR S&P 500 ETF Trust (SPY)",
        "description": (
            "Fondo cotizado que replica el índice S&P 500; sirve como "
            "referencia del mercado accionario estadounidense en conjunto."
        ),
    },
    "NBIS": {
        "name": "Nebius Group N.V.",
        "description": (
            "Empresa de infraestructura en la nube y servicios para "
            "inteligencia artificial; perfil de crecimiento tecnológico."
        ),
    },
    "RKLB": {
        "name": "Rocket Lab Corporation",
        "description": (
            "Compañía aeroespacial que lanza satélites y desarrolla "
            "sistemas espaciales; sector alta tecnología y defensa."
        ),
    },
    "IYW": {
        "name": "iShares US Technology ETF (IYW)",
        "description": (
            "ETF que agrupa acciones tecnológicas de EE. UU.; refleja el "
            "sector tech más que una sola empresa."
        ),
    },
    "AAPL": {
        "name": "Apple Inc.",
        "description": (
            "Fabricante de iPhone, Mac y servicios digitales; una de las "
            "mayores capitalizaciones del mercado tecnológico."
        ),
    },
    "DAL": {
        "name": "Delta Air Lines, Inc.",
        "description": (
            "Aerolínea estadounidense de pasajeros y carga; sensible a "
            "precio del combustible y demanda de viajes."
        ),
    },
}

DATAFRAME_COLUMNS: dict[str, str] = {
    "Open": "Apertura",
    "High": "Máximo",
    "Low": "Mínimo",
    "Close": "Cierre",
    "Volume": "Volumen",
    "SMA20": "Media móvil 20",
    "SMA50": "Media móvil 50",
    "SMA_CROSS_BULL": "Cruce alcista (MM 20 sobre 50)",
    "SMA_CROSS_BEAR": "Cruce bajista (MM 20 bajo 50)",
    "DOJISTAR": "Señal estrella Doji",
    "HARAMI": "Señal Harami",
    "HAMMER": "Señal martillo",
    "INVERTEDHAMMER": "Señal martillo invertido",
    "SHOOTINGSTAR": "Señal estrella fugaz",
    "ENGULFING": "Señal envolvente",
}

SMA_CROSS: dict[str, dict[str, str]] = {
    "bull": {
        "description": (
            "La media rápida de 20 días pasa por encima de la de 50 días. "
            "Suele mirarse como un posible giro hacia impulso alcista."
        ),
    },
    "bear": {
        "description": (
            "La media de 20 días pasa por debajo de la de 50 días. "
            "Suele mirarse como un posible giro hacia impulso bajista."
        ),
    },
}


def s(key: str, **kwargs: Any) -> str:
    text = STRINGS[key]
    return text.format(**kwargs) if kwargs else text


def pattern(key: str) -> dict[str, str]:
    return PATTERNS[key]


def chart(key: str) -> str:
    return CHART[key]


def sma_cross_text(kind: str) -> dict[str, str]:
    data = SMA_CROSS[kind]
    return {
        "label": chart(f"sma_cross_{kind}"),
        "description": data["description"],
    }


def considerations() -> str:
    return CONSIDERATIONS


def ticker_catalog(symbol: str) -> dict[str, str]:
    return TICKER_CATALOG[symbol.upper()]


def label_dataframe_column(column: str) -> str:
    return DATAFRAME_COLUMNS.get(column, column)


def fib_price_column(column: str) -> str:
    mapping = {
        "Close": "fib_price_close",
        "High": "fib_price_high",
        "Low": "fib_price_low",
    }
    return s(mapping[column])
