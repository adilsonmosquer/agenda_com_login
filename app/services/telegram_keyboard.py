def teclado_evento(evento):

    return {

        "inline_keyboard": [

            [

                {

                    "text": "✅ Concluir",

                    "callback_data": f"concluir:{evento.id}"

                },

                {

                    "text": "📌 Pendente",

                    "callback_data": f"pendente:{evento.id}"

                }

            ],

            [

                {

                    "text": "🗑 Excluir",

                    "callback_data": f"excluir:{evento.id}"

                }

            ]

        ]

    }