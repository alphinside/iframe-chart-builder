BARCHART_REQUEST_EXAMPLES = {
    "long_format": {
        "summary": "vertical bar chart long data format",
        "value": {
            "table_name": "example_bar_long",
            "chart_name": "example_bar_long",
            "chart_params": {
                "title": "Medal Winnings",
                "color_opt": {
                    "discrete": {
                        "group": "qualitative",
                        "color_name": "Prism",
                    },
                    "continuous": {
                        "group": "sequential",
                        "color_name": "Rainbow",
                    },
                },
                "column_for_x": "nation",
                "column_for_y": "count",
                "column_for_color": "medal",
                "barmode": "stack",
                "orientation": "vertical",
                "filters": [
                    {"column": "medal", "type": "categorical"},
                    {"column": "count", "type": "numerical"},
                ],
            },
        },
    },
    "long_format_horizontal": {
        "summary": "horizontal bar chart long data format",
        "value": {
            "table_name": "example_bar_long",
            "chart_name": "example_bar_long_horizontal",
            "chart_params": {
                "title": "Medal Winnings",
                "color_opt": {
                    "discrete": {
                        "group": "qualitative",
                        "color_name": "Prism",
                    },
                    "continuous": {
                        "group": "sequential",
                        "color_name": "Rainbow",
                    },
                },
                "column_for_x": "count",
                "column_for_y": "nation",
                "column_for_color": "medal",
                "barmode": "stack",
                "orientation": "horizontal",
                "filters": [
                    {"column": "medal", "type": "categorical"},
                    {"column": "count", "type": "numerical"},
                ],
            },
        },
    },
    "wide_format": {
        "summary": "vertical bar chart wide data format",
        "value": {
            "table_name": "example_bar_wide",
            "chart_name": "example_bar_wide",
            "chart_params": {
                "title": "Medal Winnings",
                "color_opt": {
                    "discrete": {
                        "group": "qualitative",
                        "color_name": "Prism",
                    },
                    "continuous": {
                        "group": "sequential",
                        "color_name": "Rainbow",
                    },
                },
                "column_for_x": "nation",
                "column_for_y": ["bronze", "silver", "gold"],
                "barmode": "stack",
                "orientation": "vertical",
                "filters": [
                    {"column": "bronze", "type": "numerical"},
                    {"column": "silver", "type": "numerical"},
                    {"column": "gold", "type": "numerical"},
                ],
            },
        },
    },
    "wide_format_horizontal": {
        "summary": "horizontal bar chart wide data format",
        "value": {
            "table_name": "example_bar_wide",
            "chart_name": "example_bar_wide_horizontal",
            "chart_params": {
                "title": "Medal Winnings",
                "color_opt": {
                    "discrete": {
                        "group": "qualitative",
                        "color_name": "Prism",
                    },
                    "continuous": {
                        "group": "sequential",
                        "color_name": "Rainbow",
                    },
                },
                "column_for_x": ["bronze", "silver", "gold"],
                "column_for_y": "nation",
                "barmode": "stack",
                "orientation": "horizontal",
                "filters": [
                    {"column": "bronze", "type": "numerical"},
                    {"column": "silver", "type": "numerical"},
                    {"column": "gold", "type": "numerical"},
                ],
            },
        },
    },
}

CHOROPLETHMAP_REQUEST_EXAMPLES = {
    "default": {
        "value": {
            "table_name": "example_choropleth_map",
            "chart_name": "example_choropleth_map",
            "chart_params": {
                "title": "Indonesia Population",
                "color_opt": {
                    "discrete": {
                        "group": "qualitative",
                        "color_name": "Prism",
                    },
                    "continuous": {
                        "group": "sequential",
                        "color_name": "Rainbow",
                    },
                },
                "column_for_location": "state",
                "column_for_color": "residents",
                "zoom_level": 4,
                "filters": [
                    {"column": "state", "type": "categorical"},
                    {"column": "residents", "type": "numerical"},
                ],
            },
        }
    }
}

BUBBLEMAP_REQUEST_EXAMPLES = {
    "default": {
        "value": {
            "table_name": "example_bubble_map",
            "chart_name": "example_bubble_map",
            "chart_params": {
                "title": "Indonesia Population",
                "color_opt": {
                    "discrete": {
                        "group": "qualitative",
                        "color_name": "Prism",
                    },
                    "continuous": {
                        "group": "sequential",
                        "color_name": "Rainbow",
                    },
                },
                "column_for_latitude": "latitude",
                "column_for_longitude": "longitude",
                "column_for_color": "name",
                "column_for_size": "residents",
                "zoom_level": 4,
                "filters": [
                    {"column": "name", "type": "categorical"},
                    {"column": "residents", "type": "numerical"},
                ],
            },
        }
    }
}

BUBBLECHART_REQUEST_EXAMPLES = {
    "default": {
        "value": {
            "table_name": "example_bubble_chart",
            "chart_name": "example_bubble_chart",
            "chart_params": {
                "title": "Gap Minder",
                "color_opt": {
                    "discrete": {
                        "group": "qualitative",
                        "color_name": "Prism",
                    },
                    "continuous": {
                        "group": "sequential",
                        "color_name": "Rainbow",
                    },
                },
                "column_for_x": "gdpPercap",
                "column_for_y": "lifeExp",
                "column_for_color": "continent",
                "column_for_size": "pop",
                "column_for_hover_name": "country",
                "apply_log_x": False,
                "bubble_size_max": 60,
                "filters": [
                    {"column": "lifeExp", "type": "numerical"},
                    {"column": "gdpPercap", "type": "numerical"},
                    {"column": "pop", "type": "numerical"},
                    {"column": "continent", "type": "categorical"},
                ],
            },
        }
    }
}

LINECHART_REQUEST_EXAMPLES = {
    "default": {
        "value": {
            "table_name": "example_line_chart",
            "chart_name": "example_line_chart",
            "chart_params": {
                "title": "Gap Minder",
                "color_opt": {
                    "discrete": {
                        "group": "qualitative",
                        "color_name": "Prism",
                    },
                },
                "column_for_x": "year",
                "column_for_y": "lifeExp",
                "column_for_color": "country",
                "filters": [
                    {"column": "lifeExp", "type": "numerical"},
                    {"column": "continent", "type": "categorical"},
                ],
            },
        }
    }
}

PIECHART_REQUEST_EXAMPLES = {
    "default": {
        "value": {
            "table_name": "example_pie_chart",
            "chart_name": "example_pie_chart",
            "chart_params": {
                "title": "Gap Minder",
                "color_opt": {
                    "discrete": {
                        "group": "qualitative",
                        "color_name": "Prism",
                    },
                },
                "column_for_values": "pop",
                "column_for_names": "country",
                "center_hole_ratio": 0.3,
                "filters": [
                    {"column": "country", "type": "categorical"},
                ],
            },
        }
    }
}

WINDROSECHART_REQUEST_EXAMPLES = {
    "default": {
        "value": {
            "table_name": "example_windrose_chart",
            "chart_name": "example_windrose_chart",
            "chart_params": {
                "title": "Wind Distribution",
                "color_opt": {
                    "discrete": {
                        "group": "qualitative",
                        "color_name": "Prism",
                    },
                    "continuous": {
                        "group": "sequential",
                        "color_name": "Rainbow",
                    },
                },
                "column_for_radius": "frequency",
                "column_for_theta": "direction",
                "column_for_color": "strength",
            },
        }
    }
}

SUNBURSTCHART_REQUEST_EXAMPLES = {
    "default": {
        "value": {
            "table_name": "example_sunburst_chart",
            "chart_name": "example_sunburst_chart",
            "chart_params": {
                "title": "Tips Distribution",
                "color_opt": {
                    "discrete": {
                        "group": "qualitative",
                        "color_name": "Prism",
                    },
                    "continuous": {
                        "group": "sequential",
                        "color_name": "Rainbow",
                    },
                },
                "column_for_path": ["sex", "day", "time"],
                "column_for_values": "total_bill",
                "column_for_color": "day",
                "filters": [
                    {"column": "sex", "type": "categorical"},
                    {"column": "day", "type": "categorical"},
                    {"column": "time", "type": "categorical"},
                ],
            },
        }
    }
}

RADARCHART_REQUEST_EXAMPLES = {
    "default": {
        "value": {
            "table_name": "example_radar_chart",
            "chart_name": "example_radar_chart",
            "chart_params": {
                "title": "Product Attributes",
                "color_opt": {
                    "discrete": {
                        "group": "qualitative",
                        "color_name": "Prism",
                    },
                },
                "column_for_radius": "products",
                "column_for_theta": [
                    "processing_cost",
                    "mechanical_properties",
                    "chemical_stability",
                    "thermal_stability",
                    "device_integration",
                ],
                "fill": "toself",
            },
        }
    }
}
