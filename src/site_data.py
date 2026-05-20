site = {
    "name": "Max Sepúlveda",
    "title_suffix": {"es": "Portfolio", "en": "Portfolio"},
    "description": {
        "es": "Portfolio de Max Sepúlveda, artista visual, artesano y gestor cultural chileno.",
        "en": "Portfolio of Max Sepúlveda, Chilean visual artist, artisan and cultural manager.",
    },
    "tagline": {
        "es": "Artista visual · Artesano · Gestor cultural",
        "en": "Visual artist · Artisan · Cultural manager",
    },
    "email": "maxsepulvedaz@gmail.com",
    "year": "2026",
}


def image(source, path, alt_es, alt_en, caption_es=None, caption_en=None):
    return {
        "source": source,
        "src": f"assets/images/gallery/{path}",
        "alt": {"es": alt_es, "en": alt_en},
        "caption": {"es": caption_es or alt_es, "en": caption_en or alt_en},
    }


biography_images = [
    image(
        "Fotos Web anterior/Curriculum – Max Sepúlveda/imgi_3_Artista-Max-Sepulveda.jpg",
        "biografia/max-sepulveda-retrato.jpg",
        "Retrato de Max Sepúlveda",
        "Portrait of Max Sepúlveda",
    ),
    image(
        "Fotos Web anterior/Curriculum – Max Sepúlveda/imgi_8_taller_alfereria_pueblo_de_indios.jpg",
        "biografia/taller-alfareria.jpg",
        "Max Sepúlveda durante un taller de alfarería",
        "Max Sepúlveda during a pottery workshop",
    ),
    image(
        "Fotos Web anterior/Max Sepúlveda – Visual Artist from Chile/imgi_3_Exposicion_Max_Sepulveda.jpg",
        "biografia/exposicion-max-sepulveda.jpg",
        "Montaje expositivo de Max Sepúlveda",
        "Exhibition installation by Max Sepúlveda",
    ),
    image(
        "Fotos Web anterior/Max Sepúlveda – Visual Artist from Chile/imgi_19_Montaje-para-fotografía-de-la-muestra-Widufe-Kuyfiche.jpg",
        "biografia/montaje-widufe-kuyfiche.jpg",
        "Montaje para fotografía de la muestra Widüfe Kuyfiche",
        "Installation for the Widüfe Kuyfiche exhibition photograph",
    ),
    image(
        "Fotos Web anterior/Max Sepúlveda – Visual Artist from Chile/imgi_15_IMG_4559_sm.jpg",
        "biografia/proceso-taller-max-sepulveda.jpg",
        "Proceso de taller de Max Sepúlveda",
        "Max Sepúlveda workshop process",
    ),
    image(
        "Fotos Web anterior/Max Sepúlveda – Visual Artist from Chile/imgi_18_pakal-de-palenque.jpg",
        "biografia/pakal-de-palenque.jpg",
        "Obra Pakal de Palenque de Max Sepúlveda",
        "Pakal de Palenque work by Max Sepúlveda",
    ),
    image(
        "Fotos Web anterior/Max Sepúlveda – Visual Artist from Chile/imgi_20_jarron.jpg",
        "biografia/jarron-ceramico.jpg",
        "Jarrón cerámico de Max Sepúlveda",
        "Ceramic jar by Max Sepúlveda",
    ),
    image(
        "Fotos Web anterior/Max Sepúlveda – Visual Artist from Chile/imgi_21_viviendo-la-cuarentena.jpg",
        "biografia/viviendo-la-cuarentena.jpg",
        "Obra Viviendo la cuarentena de Max Sepúlveda",
        "Living the Quarantine work by Max Sepúlveda",
    ),
]

workshop_portrait_image = {
    "src": "assets/images/max-sepulveda-hero.jpg",
    "alt": {
        "es": "Max Sepúlveda trabajando una pieza de alfarería en su taller",
        "en": "Max Sepúlveda working on a pottery piece in his studio",
    },
    "caption": {
        "es": "Max Sepúlveda en su taller de alfarería",
        "en": "Max Sepúlveda in his pottery studio",
    },
}

bordado_urbano_images = [
    image("Fotos Web anterior/Antofagasta_ Urban Embroidery – Max Sepúlveda/imgi_15_DSC06481.jpg", "bordado-urbano/bordado-urbano-01.jpg", "Participantes bordando el mapa colectivo de Calama", "Participants embroidering the collective map of Calama"),
    image("Fotos Web anterior/Antofagasta_ Urban Embroidery – Max Sepúlveda/imgi_12_DSC06623.jpg", "bordado-urbano/bordado-urbano-02.jpg", "Detalle del proceso de Bordado Urbano", "Detail of the Urban Embroidery process"),
    image("Fotos Web anterior/Antofagasta_ Urban Embroidery – Max Sepúlveda/imgi_14_DSC06587.jpg", "bordado-urbano/bordado-urbano-03.jpg", "Trabajo comunitario en torno al tapiz urbano", "Community work around the urban tapestry"),
    image("Fotos Web anterior/Antofagasta_ Urban Embroidery – Max Sepúlveda/imgi_11_DSC06648.jpg", "bordado-urbano/bordado-urbano-04.jpg", "Encuentro público del proyecto Bordado Urbano", "Public gathering from the Urban Embroidery project"),
    image("Fotos Web anterior/Antofagasta_ Urban Embroidery – Max Sepúlveda/imgi_13_foto-bordado-urbano-2.jpg", "bordado-urbano/bordado-urbano-05.jpg", "Mapa textil colectivo de Calama", "Collective textile map of Calama"),
    image("Fotos Web anterior/Antofagasta_ Urban Embroidery – Max Sepúlveda/imgi_16_DSC06362.jpg", "bordado-urbano/bordado-urbano-06.jpg", "Bordado participativo en espacio público", "Participatory embroidery in public space"),
]

charrua_images = [
    image("Fotos Web anterior/Uruguay_ Charrua Embroidery – Max Sepúlveda/imgi_12_GOPR1367.jpg", "bordado-charrua/bordado-charrua-01.jpg", "Proceso colectivo del Bordado Charrúa de la Memoria", "Collective process of Charrúa Embroidery of Memory"),
    image("Fotos Web anterior/Uruguay_ Charrua Embroidery – Max Sepúlveda/imgi_13_GOPR1039.jpg", "bordado-charrua/bordado-charrua-02.jpg", "Comunidad bordando relatos del territorio", "Community embroidering stories of the territory"),
    image("Fotos Web anterior/Uruguay_ Charrua Embroidery – Max Sepúlveda/imgi_16_GOPR1042.jpg", "bordado-charrua/bordado-charrua-03.jpg", "Mapa textil de la costa de Rocha", "Textile map of the Rocha coast"),
    image("Fotos Web anterior/Uruguay_ Charrua Embroidery – Max Sepúlveda/imgi_17_GOPR1388.jpg", "bordado-charrua/bordado-charrua-04.jpg", "Participantes del proyecto en Uruguay", "Project participants in Uruguay"),
    image("Fotos Web anterior/Uruguay_ Charrua Embroidery – Max Sepúlveda/imgi_26_GOPR5208.jpg", "bordado-charrua/bordado-charrua-05.jpg", "Detalle del bordado colectivo charrúa", "Detail of the collective Charrúa embroidery"),
    image("Fotos Web anterior/Uruguay_ Charrua Embroidery – Max Sepúlveda/imgi_27_GOPR5216.jpg", "bordado-charrua/bordado-charrua-06.jpg", "Exhibición comunitaria del mapa bordado", "Community exhibition of the embroidered map"),
]

new_zealand_images = [
    image("Fotos Web anterior/New Zealand_ Workshops and Exhibition – Max Sepúlveda/imgi_25_IMG_7615.jpg", "nueva-zelanda/nueva-zelanda-01.jpg", "Taller y residencia artística en Nueva Zelanda", "Workshop and artistic residency in New Zealand"),
    image("Fotos Web anterior/New Zealand_ Workshops and Exhibition – Max Sepúlveda/imgi_31_IMG_7665.jpg", "nueva-zelanda/nueva-zelanda-02.jpg", "Obras textiles y cerámicas en Dunedin", "Textile and ceramic works in Dunedin"),
    image("Fotos Web anterior/New Zealand_ Workshops and Exhibition – Max Sepúlveda/imgi_33_IMG_7625.jpg", "nueva-zelanda/nueva-zelanda-03.jpg", "Proceso de exposición en la School of Art", "Exhibition process at the School of Art"),
    image("Fotos Web anterior/New Zealand_ Workshops and Exhibition – Max Sepúlveda/imgi_43_max-seplveda-tagua-taguas_30930615217_o.jpg", "nueva-zelanda/nueva-zelanda-04.jpg", "Piezas inspiradas en Tagua Tagua", "Pieces inspired by Tagua Tagua"),
    image("Fotos Web anterior/New Zealand_ Workshops and Exhibition – Max Sepúlveda/imgi_52_max-seplveda-tagua-taguas_31998501338_o.jpg", "nueva-zelanda/nueva-zelanda-05.jpg", "Detalle de obra en la muestra de Nueva Zelanda", "Artwork detail from the New Zealand exhibition"),
    image("Fotos Web anterior/New Zealand_ Workshops and Exhibition – Max Sepúlveda/imgi_67_max-seplveda-tagua-taguas_30930585677_o.jpg", "nueva-zelanda/nueva-zelanda-06.jpg", "Montaje de Textiles y Alfarería del Tagua Tagua", "Installation of Textiles and Pottery of Tagua Tagua"),
]

ceramic_images = [
    image("Fotos Web anterior/Ceramic Works – Max Sepúlveda/imgi_20_chemamul-1.jpg", "ceramica/ceramica-01.jpg", "Pieza cerámica inspirada en el chemamüll", "Ceramic piece inspired by the chemamüll"),
    image("Fotos Web anterior/Ceramic Works – Max Sepúlveda/imgi_21_chemamul-detalle.jpg", "ceramica/ceramica-02.jpg", "Detalle de pieza cerámica chemamüll", "Detail of a chemamüll ceramic piece"),
    image("Fotos Web anterior/Ceramic Works – Max Sepúlveda/imgi_23_jarron.jpg", "ceramica/ceramica-03.jpg", "Jarrón cerámico de Max Sepúlveda", "Ceramic jar by Max Sepúlveda"),
    image("Fotos Web anterior/Ceramic Works – Max Sepúlveda/imgi_25_monstruo-tagua-tagua.jpg", "ceramica/ceramica-04.jpg", "Pieza escultórica Monstruo Tagua Tagua", "Sculptural piece Monster of Tagua Tagua"),
    image("Fotos Web anterior/Ceramic Works – Max Sepúlveda/imgi_27_pez-1.jpg", "ceramica/ceramica-05.jpg", "Pieza cerámica con forma de pez", "Fish-shaped ceramic piece"),
    image("Fotos Web anterior/Pottery Works – Max Sepúlveda/imgi_72_Bandeja_sm.jpg", "ceramica/ceramica-06.jpg", "Bandeja de alfarería utilitaria", "Functional pottery tray"),
    image("Fotos Web anterior/Pottery Works – Max Sepúlveda/imgi_41_viluco.jpg", "ceramica/ceramica-07.jpg", "Pieza alfarera inspirada en patrimonio local", "Pottery piece inspired by local heritage"),
    image("Fotos Web anterior/Pottery Works – Max Sepúlveda/imgi_55_cuenco-chakana.jpg", "ceramica/ceramica-08.jpg", "Cuenco cerámico con diseño chakana", "Ceramic bowl with chakana design"),
]

mural_images = [
    image("Fotos Web anterior/Collaborative Textile Murals – Max Sepúlveda/imgi_19_Mural-textil-colaborativo-1.jpg", "murales/mural-01.jpg", "Mural textil colaborativo", "Collaborative textile mural"),
    image("Fotos Web anterior/Collaborative Textile Murals – Max Sepúlveda/imgi_20_Mural-textil-colaborativo-2.jpg", "murales/mural-02.jpg", "Detalle de mural textil comunitario", "Detail of a community textile mural"),
    image("Fotos Web anterior/Collaborative Textile Murals – Max Sepúlveda/imgi_21_Mural-textil-colaborativo-3.jpg", "murales/mural-03.jpg", "Paños bordados de un mural colaborativo", "Embroidered panels from a collaborative mural"),
    image("Fotos Web anterior/Collaborative Textile Murals – Max Sepúlveda/imgi_22_Mural-textil-colaborativo-4.jpg", "murales/mural-04.jpg", "Composición textil realizada por la comunidad", "Textile composition made by the community"),
    image("Fotos Web anterior/Collaborative Textile Murals – Max Sepúlveda/imgi_14_Mural-textil-colaborativo-5.jpg", "murales/mural-05.jpg", "Obra mural textil instalada en comunidad", "Textile mural work installed in community"),
    image("Fotos Web anterior/Collaborative Textile Murals – Max Sepúlveda/imgi_17_Mural-textil-Colaborativo-8.jpg", "murales/mural-06.jpg", "Proceso de creación de mural textil", "Textile mural creation process"),
]

poncho_images = [
    image("Fotos Web anterior/Ponchos – Max Sepúlveda/imgi_15_poncho-1.jpg", "ponchos/poncho-01.jpg", "Poncho textil de Max Sepúlveda", "Textile poncho by Max Sepúlveda"),
    image("Fotos Web anterior/Ponchos – Max Sepúlveda/imgi_18_poncho-4.jpg", "ponchos/poncho-02.jpg", "Poncho contemporáneo con identidad chilena", "Contemporary poncho with Chilean identity"),
    image("Fotos Web anterior/Ponchos – Max Sepúlveda/imgi_21_poncho-7.jpg", "ponchos/poncho-03.jpg", "Diseño de poncho tejido", "Woven poncho design"),
    image("Fotos Web anterior/Ponchos – Max Sepúlveda/imgi_24_poncho-10.jpg", "ponchos/poncho-04.jpg", "Colección de ponchos textiles", "Textile poncho collection"),
]

textile_jewelry_images = [
    image("Fotos Web anterior/Textile Jewelry – Max Sepúlveda/imgi_10_joyeria-textil-1.jpg", "joyeria-textil/joyeria-01.jpg", "Joyería textil artesanal", "Handcrafted textile jewelry"),
    image("Fotos Web anterior/Textile Jewelry – Max Sepúlveda/imgi_11_joyeria-textil-2.jpg", "joyeria-textil/joyeria-02.jpg", "Detalle de joyería textil", "Detail of textile jewelry"),
    image("Fotos Web anterior/Textile Jewelry – Max Sepúlveda/imgi_12_joyeria-textil-3.jpg", "joyeria-textil/joyeria-03.jpg", "Pieza de joyería textil contemporánea", "Contemporary textile jewelry piece"),
    image("Fotos Web anterior/Textile Jewelry – Max Sepúlveda/imgi_14_joyeria-textil-5.jpg", "joyeria-textil/joyeria-04.jpg", "Accesorios textiles hechos a mano", "Handmade textile accessories"),
]

silk_images = [
    image("Fotos Web anterior/Silk Painting and Tie-Dye – Max Sepúlveda/imgi_10_Pintura-en-seda-1.jpg", "pintura-seda/seda-01.jpg", "Pintura en seda realizada por Max Sepúlveda", "Silk painting by Max Sepúlveda"),
    image("Fotos Web anterior/Silk Painting and Tie-Dye – Max Sepúlveda/imgi_9_pintura-en-seda-2.jpg", "pintura-seda/seda-02.jpg", "Obra textil en pintura sobre seda", "Textile work in silk painting"),
    image("Fotos Web anterior/Silk Painting and Tie-Dye – Max Sepúlveda/imgi_14_Teñido-por-amarras-1.jpg", "pintura-seda/seda-03.jpg", "Teñido por amarras sobre textil", "Tie-dye textile work"),
    image("Fotos Web anterior/Silk Painting and Tie-Dye – Max Sepúlveda/imgi_11_teñido-por-amarras-4.jpg", "pintura-seda/seda-04.jpg", "Detalle de teñido artesanal", "Detail of handcrafted dyeing"),
]

weaving_images = [
    image("Fotos Web anterior/Weaving Art and Embroidery – Max Sepúlveda/imgi_10_altiplano.jpg", "tejido-bordado/tejido-01.jpg", "Obra textil inspirada en el altiplano", "Textile work inspired by the highlands"),
    image("Fotos Web anterior/Weaving Art and Embroidery – Max Sepúlveda/imgi_11_misiones.jpg", "tejido-bordado/tejido-02.jpg", "Tejido artístico de Max Sepúlveda", "Art weaving by Max Sepúlveda"),
    image("Fotos Web anterior/Weaving Art and Embroidery – Max Sepúlveda/imgi_12_psicodelia_sm.jpg", "tejido-bordado/tejido-03.jpg", "Bordado con composición cromática", "Embroidery with chromatic composition"),
    image("Fotos Web anterior/Weaving Art and Embroidery – Max Sepúlveda/imgi_13_Bordado_sm.jpg", "tejido-bordado/tejido-04.jpg", "Detalle de obra bordada", "Detail of an embroidered work"),
    image("Fotos Web anterior/Weaving Art and Embroidery – Max Sepúlveda/imgi_7_tejido-telar-mapuche-1.jpg", "tejido-bordado/tejido-05.jpg", "Tejido en telar de inspiración mapuche", "Mapuche-inspired loom weaving"),
]

projects = [
    {
        "title": {"es": "Bordado Urbano", "en": "Urban Embroidery"},
        "slug": "bordado-urbano",
        "date": "2012-05-15",
        "summary": {
            "es": "Proyecto de arte comunitario en Calama (2012). Los habitantes bordaron colectivamente un mapa de 3x2 metros representando sus sueños e historias.",
            "en": "Community art project in Calama (2012). Residents collectively embroidered a 3x2 meter map representing their dreams and stories.",
        },
        "featured": True,
        "live_url": "https://maxsepulvedaartevisual.com/portafolio/bordado-urbano/",
        "tags": {"es": ["Arte Comunitario", "Textil", "Calama"], "en": ["Community Art", "Textile", "Calama"]},
        "image": bordado_urbano_images[0],
        "gallery": {
            "title": {"es": "Registro visual del proyecto", "en": "Project Visual Record"},
            "items": bordado_urbano_images,
        },
        "content": [
            {
                "type": "text_section",
                "title": {"es": "Un tapiz de sueños colectivos", "en": "A Tapestry of Collective Dreams"},
                "content": {
                    "es": "<p>Proyecto de arte comunitario en el que los habitantes de Calama bordaron colectivamente un mapa de <strong>3 x 2 metros</strong> representando sus sueños e historias para la ciudad.</p><p>Fue una intervención pública realizada en distintas locaciones (ferias, paseos peatonales, mercados), acompañada por la filmación de un <strong>documental</strong> sobre la experiencia.</p><p>El resultado fue un tapiz urbano único, fruto del trabajo conjunto del artista con más de un centenar de participantes locales.</p>",
                    "en": "<p>Community art project where residents of Calama collectively embroidered a <strong>3 x 2 meter</strong> map representing their dreams and stories for the city.</p><p>It was a public intervention carried out in different locations (fairs, pedestrian walkways, markets), accompanied by the filming of a <strong>documentary</strong> about the experience.</p><p>The result was a unique urban tapestry, the fruit of collaborative work between the artist and over a hundred local participants.</p>",
                },
                "variant": "default",
            },
            {
                "type": "quote",
                "quote": {
                    "es": "El bordado es una herramienta convocante que invita a la participación de personas de todas las edades.",
                    "en": "Embroidery is a welcoming tool that invites people of all ages to participate.",
                },
                "author": "Max Sepúlveda",
                "variant": "highlight",
            },
        ],
    },
    {
        "title": {"es": "Bordado Charrúa de la Memoria", "en": "Charrúa Embroidery of Memory"},
        "slug": "bordado-charrua-de-la-memoria",
        "date": "2016-11-20",
        "summary": {
            "es": "Mapa textil colectivo de la costa de Rocha, Uruguay. Ganador de los Fondos Concursables para la Cultura del MEC uruguayo (2016).",
            "en": "Collective textile map of the coast of Rocha, Uruguay. Winner of the Competitive Funds for Culture from the Uruguayan MEC (2016).",
        },
        "featured": True,
        "live_url": "https://maxsepulvedaartevisual.com/portafolio/bordado-charrua-de-la-memoria/",
        "tags": {"es": ["Arte Comunitario", "Textil", "Uruguay", "Premios"], "en": ["Community Art", "Textile", "Uruguay", "Awards"]},
        "image": charrua_images[0],
        "gallery": {
            "title": {"es": "Mapa bordado y comunidad", "en": "Embroidered Map and Community"},
            "items": charrua_images,
        },
        "content": [
            {
                "type": "text_section",
                "title": {"es": "Rescatando la memoria costera", "en": "Rescuing Coastal Memory"},
                "content": {
                    "es": "<p>Proyecto ganador de los <strong>Fondos Concursables para la Cultura</strong> del Ministerio de Educación y Cultura de Uruguay.</p><p>Consistió en la creación de un mapa textil colectivo de la costa de Rocha, bordado in situ por habitantes y visitantes en <strong>cinco localidades costeras</strong>.</p><p>Durante el proceso, la gente fue compartiendo anécdotas sobre los lugares que dejaron huellas en sus vidas, historias de amor, aventuras y desventuras.</p>",
                    "en": "<p>Winning project of the <strong>Competitive Funds for Culture</strong> from the Ministry of Education and Culture of Uruguay.</p><p>It consisted of creating a collective textile map of the coast of Rocha, embroidered on-site by residents and visitors in <strong>five coastal towns</strong>.</p><p>During the process, people shared anecdotes about places that left marks on their lives, stories of love, adventures and misadventures.</p>",
                },
                "variant": "default",
            },
        ],
    },
    {
        "title": {"es": "Textiles y Alfarería del Tagua Tagua", "en": "Textiles and Pottery of Tagua Tagua"},
        "slug": "textiles-y-alfareria-del-tagua-tagua",
        "date": "2018-08-10",
        "summary": {
            "es": "Exposición individual en la School of Art de Dunedin, Nueva Zelanda (2018). Diálogo entre la identidad cultural de Tagua Tagua y la tradición maorí.",
            "en": "Solo exhibition at the School of Art in Dunedin, New Zealand (2018). Dialogue between the cultural identity of Tagua Tagua and Māori tradition.",
        },
        "featured": True,
        "live_url": "https://maxsepulvedaartevisual.com/portafolio/residencia-artistica-en-nueva-zelanda/",
        "tags": {"es": ["Exposición", "Internacional", "Nueva Zelanda", "Cerámica", "Textil"], "en": ["Exhibition", "International", "New Zealand", "Ceramics", "Textile"]},
        "image": new_zealand_images[0],
        "gallery": {
            "title": {"es": "Residencia y exposición", "en": "Residency and Exhibition"},
            "items": new_zealand_images,
        },
        "content": [
            {
                "type": "text_section",
                "title": {"es": "Intercambio Cultural Chile-Nueva Zelanda", "en": "Chile-New Zealand Cultural Exchange"},
                "content": {
                    "es": "<p>Exposición individual realizada en la <strong>School of Art de Dunedin</strong>, como resultado de una residencia artística en Nueva Zelanda.</p><p>La muestra presentó una selección de obras en cerámica y textil inspiradas en la identidad cultural de <strong>Tagua Tagua</strong> y su diálogo con la tradición maorí.</p>",
                    "en": "<p>Solo exhibition held at the <strong>School of Art in Dunedin</strong>, as the result of an artistic residency in New Zealand.</p><p>The show presented a selection of ceramic and textile works inspired by the cultural identity of <strong>Tagua Tagua</strong> and its dialogue with Māori tradition.</p>",
                },
                "variant": "default",
            },
        ],
    },
    {
        "title": {"es": "Widüfe Kuyfiche – Alfarero Ancestral", "en": "Widüfe Kuyfiche – Ancestral Potter"},
        "slug": "widufe-kuyfiche-alfarero-ancestral",
        "date": "2006-03-01",
        "summary": {
            "es": "Investigación y rescate de la alfarería indígena de la zona central de Chile. Proyecto FONDART 2006.",
            "en": "Research and rescue of indigenous pottery from central Chile. FONDART 2006 project.",
        },
        "featured": True,
        "tags": {"es": ["Investigación", "Cerámica", "Fondart", "Patrimonio"], "en": ["Research", "Ceramics", "Fondart", "Heritage"]},
        "image": ceramic_images[0],
        "gallery": {
            "title": {"es": "Cerámica y alfarería", "en": "Ceramics and Pottery"},
            "items": ceramic_images,
        },
        "content": [
            {
                "type": "text_section",
                "title": {"es": "Hacedores de Greda", "en": "Clay Makers"},
                "content": {
                    "es": "<p>Proyecto financiado por el <strong>Fondo Nacional de Desarrollo Cultural y las Artes (FONDART)</strong>.</p><p>Consistió en una investigación y rescate de la alfarería indígena de la zona central de Chile, que culminó en una exposición exhibida en la <strong>Sala Samuel Román</strong> de la Casa de la Cultura de Rancagua.</p><p><em>Widüfe</em> en mapudungun significa 'alfarero' o 'hacedor de greda'.</p>",
                    "en": "<p>Project funded by the <strong>National Fund for Cultural Development and the Arts (FONDART)</strong>.</p><p>It consisted of research and rescue of indigenous pottery from central Chile, culminating in an exhibition at the <strong>Sala Samuel Román</strong> at the Casa de la Cultura in Rancagua.</p><p><em>Widüfe</em> in Mapudungun means 'potter' or 'clay maker'.</p>",
                },
                "variant": "default",
            },
        ],
    },
    {
        "title": {"es": "Murales Textiles Colaborativos", "en": "Collaborative Textile Murals"},
        "slug": "murales-textiles-colaborativos",
        "date": "2020-01-15",
        "summary": {
            "es": "Intervenciones donde comunidades crean murales de telas y bordados que se instalan en espacios públicos.",
            "en": "Interventions where communities create murals from fabrics and embroideries installed in public spaces.",
        },
        "featured": True,
        "tags": {"es": ["Arte Comunitario", "Textil", "Muralismo"], "en": ["Community Art", "Textile", "Murals"]},
        "image": mural_images[0],
        "gallery": {
            "title": {"es": "Murales textiles", "en": "Textile Murals"},
            "items": mural_images,
        },
        "content": [
            {
                "type": "text_section",
                "title": {"es": "Mosaicos Comunitarios", "en": "Community Mosaics"},
                "content": {
                    "es": "<p>Diversas intervenciones lideradas por Sepúlveda donde comunidades completas crean <strong>murales hechos de telas y bordados</strong>.</p><p>Un ejemplo destacado es el mural <strong>'Inti Ray'</strong> en Calama, financiado por Codelco dentro del programa Calama Participa.</p>",
                    "en": "<p>Various interventions led by Sepúlveda where entire communities create <strong>murals made of fabrics and embroideries</strong>.</p><p>A standout example is the <strong>'Inti Ray'</strong> mural in Calama, funded by Codelco within the Calama Participa program.</p>",
                },
                "variant": "default",
            },
        ],
    },
    {
        "title": {"es": "Residencia Artística Alicahue", "en": "Alicahue Artistic Residency"},
        "slug": "residencia-artistica-alicahue",
        "date": "2016-10-01",
        "summary": {
            "es": "Residencia del programa Red Cultura en la Región de Valparaíso (2016), trabajando con comunidades locales.",
            "en": "Residency of the Red Cultura program in the Valparaíso Region (2016), working with local communities.",
        },
        "featured": False,
        "tags": {"es": ["Arte Comunitario", "Residencia", "Valparaíso", "Red Cultura"], "en": ["Community Art", "Residency", "Valparaíso", "Red Cultura"]},
        "image": biography_images[1],
        "gallery": {
            "title": {"es": "Procesos y talleres", "en": "Processes and Workshops"},
            "items": biography_images[:3],
        },
        "content": [
            {
                "type": "text_section",
                "title": {"es": "Arte colaborativo en el Valle de Alicahue", "en": "Collaborative Art in the Alicahue Valley"},
                "content": {
                    "es": "<p>Seleccionado por el programa <strong>Red Cultura</strong> para una residencia de arte colaborativo en Alicahue, Región de Valparaíso.</p><p>Durante esta residencia, trabajó con comunidades locales en intervenciones artísticas en el territorio.</p>",
                    "en": "<p>Selected by the <strong>Red Cultura</strong> program for a collaborative art residency in Alicahue, Valparaíso Region.</p><p>During this residency, he worked with local communities on artistic interventions in the territory.</p>",
                },
                "variant": "default",
            },
        ],
    },
]

about = {
    "intro": {
        "es": '<p><strong>Maximiliano "Max" Sepúlveda Zúñiga</strong> (n. 1974) es un artista visual, artesano y gestor cultural oriundo de San Vicente de Tagua Tagua, Chile. Su trabajo abarca <strong>alfarería, cerámica, textiles, arte colaborativo y dirección de arte audiovisual</strong>, disciplinas en las que ha desarrollado una amplia producción creativa por más de veinte años.</p><p>A lo largo de su trayectoria, Sepúlveda ha realizado talleres, seminarios y demostraciones en diversos países de América Latina. Concibe el arte comunitario y colaborativo como una herramienta de transformación social, terapia y alimento para el alma, inspirándose en los lugares y comunidades donde interviene para abordar temáticas sociales, la memoria colectiva y el patrimonio natural y cultural.</p>',
        "en": '<p><strong>Maximiliano "Max" Sepúlveda Zúñiga</strong> (b. 1974) is a visual artist, artisan and cultural manager from San Vicente de Tagua Tagua, Chile. His work encompasses <strong>pottery, ceramics, textiles, collaborative art and audiovisual art direction</strong>, disciplines in which he has developed a broad creative output for over twenty years.</p><p>Throughout his career, Sepúlveda has conducted workshops, seminars and demonstrations in various Latin American countries. He conceives community and collaborative art as a tool for social transformation, therapy and food for the soul, drawing inspiration from the places and communities where he works to address social issues, collective memory and natural and cultural heritage.</p>',
    },
    "visual_story": {
        "title": {"es": "Archivo visual", "en": "Visual Archive"},
        "description": {
            "es": "Retratos, talleres, montajes y obras que acompañan su trayectoria entre cerámica, textil y mediación cultural.",
            "en": "Portraits, workshops, installations and works that trace his path through ceramics, textiles and cultural mediation.",
        },
        "items": biography_images,
    },
    "sections": [
        {
            "title": {"es": "Obra y Estilo", "en": "Work and Style"},
            "content": {
                "es": "<p>Max Sepúlveda trabaja una variedad poco común de técnicas artesanales y artísticas. En <strong>cerámica y alfarería</strong>, elabora piezas utilitarias y escultóricas siguiendo técnicas ancestrales aprendidas de maestros alfareros. En el ámbito <strong>textil</strong>, su obra incluye bordados, telares, batik, pintura en seda, confección de ponchos tradicionales y joyería textil. Esta combinación de técnicas le permite crear obras con riqueza material, donde conviven la textura de los tejidos con la solidez de la cerámica.</p><p>La obra de Sepúlveda se caracteriza por un fuerte <strong>contenido social y comunitario</strong>. Muchas de sus creaciones son el resultado de procesos colaborativos en que involucra activamente a comunidades locales. Emplea una metodología participativa: artista y comunidad se unen para reflexionar sobre la realidad de su territorio, sus problemáticas e identidad, y a partir de ese diálogo colectivo co-crean obras de arte con un profundo sentido local.</p><p>Iniciado en los años 90, su trayectoria ha evolucionado desde la artesanía tradicional hacia propuestas de <strong>arte participativo</strong>. Hoy su obra se ubica en la intersección entre arte, artesanía y acción comunitaria, manteniendo siempre el rescate de técnicas ancestrales pero en diálogo con problemáticas contemporáneas.</p>",
                "en": "<p>Max Sepúlveda works with an uncommon variety of artisanal and artistic techniques. In <strong>ceramics and pottery</strong>, he creates utilitarian and sculptural pieces following ancestral techniques learned from master potters. In the <strong>textile</strong> realm, his work includes embroideries, looms, batik, silk painting, traditional ponchos and textile jewelry. This combination of techniques allows him to create works with material richness, where the texture of fabrics coexists with the solidity of ceramics.</p><p>Sepúlveda's work is characterized by a strong <strong>social and community content</strong>. Many of his creations are the result of collaborative processes that actively involve local communities. He employs a participatory methodology: artist and community come together to reflect on their territory's reality, issues and identity, and from this collective dialogue co-create works of art with deep local meaning.</p><p>Started in the 1990s, his trajectory has evolved from traditional craftsmanship towards <strong>participatory art</strong>. Today his work sits at the intersection of art, craft and community action, always maintaining the rescue of ancestral techniques while engaging with contemporary issues.</p>",
            },
        },
        {
            "title": {"es": "Trayectoria Internacional", "en": "International Trajectory"},
            "content": {
                "es": "<p>Max Sepúlveda ha trascendido fronteras con su arte. Ha realizado exposiciones individuales y colectivas en Chile, Argentina, Belice, Nueva Zelanda, Costa Rica, Uruguay, México y Colombia, sumando más de 50 exhibiciones a la fecha. En 2018 llevó su muestra <strong>Textiles y Alfarería del Tagua Tagua</strong> a Nueva Zelanda, convirtiéndose en uno de los pocos artistas populares chilenos en exponer en Oceanía.</p><p>Ha representado a Chile en ferias, festivales y bienales internacionales de artesanía y arte popular. En Costa Rica fue invitado al <strong>Festival Internacional de las Artes</strong> y a la <strong>Costa Rica Fashion Week 2019</strong>, donde mostró su trabajo textil aplicado al diseño de vestuario. En cada país que visita, procura entablar un diálogo creativo con la cultura local, logrando una trayectoria construida sobre el respeto intercultural y la co-creación.</p>",
                "en": "<p>Max Sepúlveda has transcended borders with his art. He has held solo and group exhibitions in Chile, Argentina, Belize, New Zealand, Costa Rica, Uruguay, Mexico and Colombia, totaling over 50 exhibitions to date. In 2018 he brought his show <strong>Textiles and Pottery of Tagua Tagua</strong> to New Zealand, becoming one of the few Chilean folk artists to exhibit in Oceania.</p><p>He has represented Chile at international craft fairs, festivals and biennials. In Costa Rica he was invited to the <strong>International Festival of the Arts</strong> and <strong>Costa Rica Fashion Week 2019</strong>, where he showcased his textile work applied to fashion design. In every country he visits, he seeks to engage in creative dialogue with the local culture, building a career founded on intercultural respect and co-creation.</p>",
            },
        },
        {
            "title": {"es": "Gestión Cultural", "en": "Cultural Management"},
            "content": {
                "es": "<p>Además de su producción artística, Sepúlveda desempeña un importante rol como <strong>gestor cultural</strong>, impulsando proyectos que empoderan a las comunidades a través del arte. Su enfoque está orientado a trabajar a la par y de forma transversal con la comunidad, generando espacios de reflexión social y cooperación colectiva.</p><p>Ha trabajado con instituciones como el <strong>Museo Violeta Parra</strong>, la <strong>Fundación Superación de la Pobreza</strong> y programas como <strong>Red Cultura</strong>. Ha coordinado talleres formativos, proyectos de rescate patrimonial y cápsulas educativas en línea. Su labor como curador y organizador de muestras se evidencia en la creación de exposiciones itinerantes con las obras realizadas por comunidades.</p><p>Un sello de su gestión cultural es la <strong>inclusión y la horizontalidad</strong>. En sus residencias colaborativas, adopta el rol de facilitador más que de director, propiciando que las ideas de la gente fluyan hacia la obra.</p>",
                "en": "<p>Beyond his artistic production, Sepúlveda plays an important role as a <strong>cultural manager</strong>, promoting projects that empower communities through art. His approach focuses on working alongside and across the community, generating spaces for social reflection and collective cooperation.</p><p>He has worked with institutions such as the <strong>Museo Violeta Parra</strong>, the <strong>Fundación Superación de la Pobreza</strong> and programs like <strong>Red Cultura</strong>. He has coordinated training workshops, heritage rescue projects and online educational capsules. His work as curator and organizer is evident in the creation of traveling exhibitions featuring works made by communities.</p><p>A hallmark of his cultural management is <strong>inclusion and horizontality</strong>. In his collaborative residencies, he adopts the role of facilitator rather than director, allowing people's ideas to flow into the artwork.</p>",
            },
        },
        {
            "title": {"es": "Hitos y Reconocimientos", "en": "Milestones and Recognition"},
            "content": {
                "es": "<ul><li><strong>2006</strong> — Obtiene un Fondart Regional para <em>Widüfe Kuyfiche – Alfarero Ancestral</em>, proyecto de rescate de la cerámica tradicional.</li><li><strong>2012</strong> — Ejecuta <em>Bordado Urbano</em> en Calama, innovadora intervención de arte público colaborativo.</li><li><strong>2015</strong> — Incluido en el Catálogo Nacional de Artesanía del Consejo Nacional de la Cultura.</li><li><strong>2016</strong> — Su proyecto <em>Bordado Charrúa de la Memoria</em> gana los Fondos Concursables del MEC uruguayo.</li><li><strong>2018</strong> — Realiza residencia artística y exposición individual en la Escuela de Arte de Dunedin, Nueva Zelanda.</li><li><strong>2019</strong> — Participa en la Costa Rica Fashion Week presentando creaciones textiles con identidad chilena.</li><li><strong>2020</strong> — Incluido en el Catálogo Artesanía en Pandemia del Ministerio de las Culturas de Chile.</li><li><strong>2022</strong> — Recibe homenaje en la región de O'Higgins por su aporte al desarrollo cultural local.</li></ul>",
                "en": "<ul><li><strong>2006</strong> — Receives a Fondart Regional grant for <em>Widüfe Kuyfiche – Ancestral Potter</em>, a project rescuing traditional ceramics.</li><li><strong>2012</strong> — Executes <em>Urban Embroidery</em> in Calama, an innovative public collaborative art intervention.</li><li><strong>2015</strong> — Included in the National Crafts Catalog of the National Council for Culture.</li><li><strong>2016</strong> — His project <em>Charrúa Embroidery of Memory</em> wins the Competitive Funds from the Uruguayan MEC.</li><li><strong>2018</strong> — Completes an artistic residency and solo exhibition at the Dunedin School of Art, New Zealand.</li><li><strong>2019</strong> — Participates in Costa Rica Fashion Week presenting textile creations with Chilean identity.</li><li><strong>2020</strong> — Included in the Crafts in Pandemic Catalog of the Chilean Ministry of Cultures.</li><li><strong>2022</strong> — Receives tribute in the O'Higgins region for his contribution to local cultural development.</li></ul>",
            },
        },
        {
            "title": {"es": "Entrevistas y Publicaciones", "en": "Interviews and Publications"},
            "content": {
                "es": "<p>La propuesta artística de Max Sepúlveda ha sido difundida en diversos medios. Fue protagonista del cuarto episodio de <strong>Artefacto</strong>, serie dedicada al arte regional chileno. Sus proyectos <em>Bordado Urbano</em> y <em>Bordado Charrúa</em> cuentan con documentales propios que registran los procesos creativos comunitarios.</p><p>Ha sido incluido en el <strong>Catálogo Nacional de Artesanía 2015</strong> y colaboró con el libro <strong>Arte Textil y Resistencia</strong> (ed. Universidad de Chile, 2021), donde se analiza el rol del bordado en movimientos sociales.</p>",
                "en": "<p>Max Sepúlveda's artistic proposal has been featured in various media. He was the protagonist of the fourth episode of <strong>Artefacto</strong>, a series dedicated to Chilean regional art. His projects <em>Urban Embroidery</em> and <em>Charrúa Embroidery</em> have their own documentaries that record the community creative processes.</p><p>He has been included in the <strong>National Crafts Catalog 2015</strong> and collaborated on the book <strong>Textile Art and Resistance</strong> (ed. University of Chile, 2021), which analyzes the role of embroidery in social movements.</p>",
            },
        },
    ],
}

gallery_sections = [
    {
        "title": {"es": "Cerámica y alfarería", "en": "Ceramics and Pottery"},
        "description": {"es": "Piezas utilitarias, escultóricas y obras inspiradas en el patrimonio local.", "en": "Functional pieces, sculptural works and objects inspired by local heritage."},
        "items": ceramic_images,
    },
    {
        "title": {"es": "Bordado y arte comunitario", "en": "Embroidery and Community Art"},
        "description": {"es": "Procesos colectivos donde el textil activa memoria, encuentro y participación.", "en": "Collective processes where textiles activate memory, encounter and participation."},
        "items": bordado_urbano_images[:3] + charrua_images[:3],
    },
    {
        "title": {"es": "Murales textiles colaborativos", "en": "Collaborative Textile Murals"},
        "description": {"es": "Obras de gran formato construidas con paños, bordados y relatos comunitarios.", "en": "Large-format works built from fabric panels, embroidery and community stories."},
        "items": mural_images,
    },
    {
        "title": {"es": "Textiles, ponchos y joyería", "en": "Textiles, Ponchos and Jewelry"},
        "description": {"es": "Diseño textil, vestuario, accesorios y piezas de oficio contemporáneo.", "en": "Textile design, clothing, accessories and contemporary craft pieces."},
        "items": weaving_images[:3] + poncho_images[:3] + textile_jewelry_images[:3],
    },
    {
        "title": {"es": "Pintura en seda y teñidos", "en": "Silk Painting and Dyeing"},
        "description": {"es": "Color, gráfica e iconografía aplicados a soportes textiles.", "en": "Color, graphic language and iconography applied to textile supports."},
        "items": silk_images,
    },
    {
        "title": {"es": "Procesos, talleres y exposiciones", "en": "Processes, Workshops and Exhibitions"},
        "description": {"es": "Momentos de taller, montaje, residencia y mediación cultural.", "en": "Moments from workshops, installations, residencies and cultural mediation."},
        "items": biography_images + new_zealand_images[:4],
    },
]

home_blocks = [
    {
        "type": "hero",
        "title": "Max Sepúlveda",
        "subtitle": {"es": "Artista Visual, Artesano y Gestor Cultural", "en": "Visual Artist, Artisan and Cultural Manager"},
        "cta": {
            "text": {"es": "Ver Proyectos", "en": "View Projects"},
            "url": {"es": "/es/proyectos/", "en": "/en/projects/"},
        },
        "variant": "default",
    },
    {
        "type": "text_section",
        "title": {"es": "Biografía", "en": "Biography"},
        "content": {
            "es": "<p><strong>Maximiliano 'Max' Sepúlveda Zúñiga</strong> (n. 1974) es un artista visual, artesano y gestor cultural oriundo de San Vicente de Tagua Tagua, Chile. Su trabajo abarca <strong>alfarería, cerámica, textiles, arte colaborativo y dirección de arte audiovisual</strong>, disciplinas en las que ha desarrollado una amplia producción creativa por más de veinte años.</p><p>Se formó junto a maestros artesanos y artistas visuales de Latinoamérica, complementando su aprendizaje en instituciones de Chile, Argentina y México. Concibe el arte comunitario y colaborativo como una herramienta de transformación social, terapia y alimento para el alma, inspirándose en los lugares y comunidades donde interviene para abordar temáticas sociales, la memoria colectiva y el patrimonio natural y cultural.</p><p><a href=\"/es/biografia/\" class=\"btn\">Conoce más sobre mi trayectoria</a></p>",
            "en": "<p><strong>Maximiliano 'Max' Sepúlveda Zúñiga</strong> (b. 1974) is a visual artist, artisan and cultural manager from San Vicente de Tagua Tagua, Chile. His work encompasses <strong>pottery, ceramics, textiles, collaborative art and audiovisual art direction</strong>, disciplines in which he has developed a broad creative output for over twenty years.</p><p>He trained alongside master artisans and visual artists from Latin America, complementing his learning in institutions in Chile, Argentina and Mexico. He conceives community and collaborative art as a tool for social transformation, therapy and food for the soul, drawing inspiration from the places and communities where he works to address social issues, collective memory and natural and cultural heritage.</p><p><a href=\"/en/biography/\" class=\"btn\">Learn more about my trajectory</a></p>",
        },
        "image": workshop_portrait_image,
        "image_position": "right",
        "variant": "default",
    },
    {
        "type": "quote",
        "quote": {
            "es": "Vincular a la comunidad desde la sensibilidad, generando lazos que van más allá de lo cotidiano. El arte comunitario y colaborativo es una herramienta de transformación social.",
            "en": "Connecting with the community through sensitivity, creating bonds that go beyond the everyday. Community and collaborative art is a tool for social transformation.",
        },
        "author": "Max Sepúlveda",
        "source": {"es": "Filosofía de Arte Colaborativo", "en": "Collaborative Art Philosophy"},
        "variant": "highlight",
    },
    {
        "type": "media_strip",
        "title": {"es": "Oficios, materia y territorio", "en": "Craft, Matter and Territory"},
        "subtitle": {"es": "Una mirada visual a las técnicas que atraviesan su obra.", "en": "A visual look at the techniques that run through his work."},
        "items": [ceramic_images[3], weaving_images[4], silk_images[0], textile_jewelry_images[0]],
        "variant": "muted",
    },
    {
        "type": "text_section",
        "title": {"es": "Gestión Cultural", "en": "Cultural Management"},
        "content": {
            "es": "<p>Como gestor cultural, Max Sepúlveda impulsa proyectos que empoderan a las comunidades. Trabaja <em>a la par y de forma transversal con la comunidad</em>, generando espacios de reflexión social y cooperación colectiva.</p><p>Ha trabajado con instituciones como el <strong>Museo Violeta Parra</strong>, la <strong>Fundación Superación de la Pobreza</strong> y programas como <strong>Red Cultura</strong>.</p>",
            "en": "<p>As a cultural manager, Max Sepúlveda promotes projects that empower communities. He works <em>alongside and across the community</em>, generating spaces for social reflection and collective cooperation.</p><p>He has worked with institutions such as the <strong>Museo Violeta Parra</strong>, the <strong>Fundación Superación de la Pobreza</strong> and programs like <strong>Red Cultura</strong>.</p>",
        },
        "image": biography_images[1],
        "image_position": "left",
        "variant": "default",
    },
    {
        "type": "media_strip",
        "title": {"es": "Procesos colaborativos", "en": "Collaborative Processes"},
        "subtitle": {"es": "Bordados, murales y encuentros donde la comunidad se vuelve autora.", "en": "Embroidery, murals and gatherings where the community becomes the author."},
        "items": [bordado_urbano_images[1], charrua_images[2], mural_images[1]],
        "variant": "default",
    },
    {
        "type": "portfolio_grid",
        "title": {"es": "Proyectos Destacados", "en": "Featured Projects"},
        "subtitle": {"es": "Arte comunitario, cerámica y textiles", "en": "Community art, ceramics and textiles"},
        "show_featured_only": True,
        "max_items": 6,
        "show_link_to_all": True,
        "variant": "default",
    },
    {
        "type": "media_strip",
        "title": {"es": "Archivo visual de obra", "en": "Visual Work Archive"},
        "subtitle": {"es": "Textiles, alfarería, vestuario y registros de exposición listos para explorar.", "en": "Textiles, pottery, garments and exhibition records ready to explore."},
        "items": [new_zealand_images[2], poncho_images[1], ceramic_images[5], biography_images[2]],
        "variant": "muted",
    },
    {
        "type": "gallery",
        "title": {"es": "Galería seleccionada", "en": "Selected Gallery"},
        "subtitle": {"es": "Cerámica, textiles, bordados y procesos de taller", "en": "Ceramics, textiles, embroidery and workshop processes"},
        "items": [
            ceramic_images[2],
            bordado_urbano_images[0],
            charrua_images[0],
            mural_images[0],
            poncho_images[0],
            silk_images[0],
        ],
        "columns": 3,
        "show_link_to_all": True,
        "variant": "default",
    },
    {
        "type": "contact",
        "title": {"es": "Contacto", "en": "Contact"},
        "text": {
            "es": "¿Interesado en colaborar, contratar un taller o adquirir obras? No dudes en escribirme.",
            "en": "Interested in collaborating, booking a workshop or purchasing artwork? Feel free to reach out.",
        },
        "email": "maxsepulvedaz@gmail.com",
        "social_links": [
            {"platform": "instagram", "url": "https://instagram.com/maxartevisual", "label": {"es": "Instagram", "en": "Instagram"}},
            {"platform": "website", "url": "https://maxsepulvedaartevisual.com", "label": {"es": "Sitio web", "en": "Website"}},
        ],
        "variant": "default",
    },
]
