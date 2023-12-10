% References to ACM TEI 2007 content
% Brygg Ullmer, Clemson University
% Begun 2023-11-16


content:
  program:     https://tei.acm.org/2007/program.html
  overview: 
    addresses: [https://tei.acm.org/2007/program/TwoMinuteMadness_1.pdf,
                https://tei.acm.org/2007/program/TwoMinuteMadness_2.pdf]

%%%%%%%%%%%%%%%%%%%%%%%% Themes 1 %%%%%%%%%%%%%%%%%%%%%%%%

schema(themes1, [title, abbrev, chapter, sessions, chair]).

themes1('Connectedness', co, [bwd, er, mg, mo, snkbsars, bwd, mg, mk ehlo, rtsi, zhsj],
                             [[er, mo], [zhsj, snkbsars, bwd, mg]], ['Ali Mazalek', 'Martin Kaltenbrunner']).

themes1('Integrating the Virtual and the Physical', ivp, 
               [vg, sn, pa, mb, dkm, eng, db, lcgs, lkm, svgs],  [pa, svgs, sn, eng],      'Trevor Pering').

themes1('The Expressive Character of Interaction', eci,
               [sh, mn, hfamop, re, hi, cgzi, jgak, sm, bvhhb],  [hamop, slelo, cgzi, hi], 'Peter Gall Krogh').

themes1('Learning through Physical Interaction', lpi,
             [hhvbm, hj, ma, daw, dh, gtshesj, vfh, km, an],     [ma, km, hhv, an],        'Orit Shaer').

themes1('Context Dependency and Physical Adaptability', cdpa,
             [pno, kmhbrbrs, bi, sscb, mrgak],                   [scb, mrgk, pno, b],      'Nicolas Villar').

themes1('Body Movements', bm,
             [je, fr, shs, mo, paw, rhkcl, lre, bsh],            [paw, rhkcl, lre, m],     'Thecla Schiphorst').

%%%%%%%%%%%%%%%%%%%%%%%% Sessions %%%%%%%%%%%%%%%%%%%%%%%%

schema(session, [title, abbrev, papers, chair]).

session('Two Minute Madness (1)', tmm1, [ehl, lkm, db, lcgs, bvhhb, r, jgak, hj, dh, daw, ss, j],    'Matthias Kranz').
session('Two Minute Madness (2)', tmm2, [rtsi, kb, mkm, vg, s, mn, s, vfh, gshesj, f, bsh, kmhrbrs], 'Matthias Kranz').

%%%%%%%%%%%%%%%%%%%%%%%% Continents %%%%%%%%%%%%%%%%%%%%%%%%

schema(continent, [name, abbrev1, abbrev2, countries]).

continent('Europe',        europe,   E, [germany, uk, denmark, netherlands, sweden, switzerland, spain, finland, italy]).
continent('Asia',          asia,     I, [japan, southKorea]).
continent('Africa',        africa,   F, [southAfrica]).
continent('Oceania',       oceania,  O, [newZealand, australia]).
continent('North America', namerica, N, [usa, canada]).
continent('South America', samerica, S, [colombia]).

%%%%%%%%%%%%%%%%%%%%%%%% Themes 2 %%%%%%%%%%%%%%%%%%%%%%%%

schema(themes2, [title, abbrev, keywords, numPapers]).

themes2('Tangible UI', tangible_ui, [tui, tangibility, tangible_UIs, tangible_computing, tangible_interaction, 
                       tangible_interface, tangible_interfaces, tangible_user_interface, tangible_user_interfaces],    24).

themes2(paradigms, [augmented_reality, distributed_physical_user_interfaces, paper_user_interface, 
                     ubiquitous_computing, responsive_environments, spatial_interaction, siftable_computing_interface, 
                     tabletop_sensing, tabletop_interaction, tabletop_interfaces],                                     11).

themes2(interaction, [interaction_techniques, interaction, interactive_book, interactive_installation, 
                                     interactive_toys, explicit_interaction, interactive_video_and_sound_installation, 
                                     embedded_interaction],                                                            11).

themes2(design,    [design_process, design_research, design, interaction_design, product_design, communication_design, 
                                                                                                    complex_products], 10).

themes2(education, [montessori_inspired_manipulatives, children, digital_manipulatives, manipulatives,
                                 learning_toys, learning, education, educational_game, edutainment],                   10).

themes2(evaluation, [case_studies, evaluation, participatory_design, experience, usability, use_qualities, 
                               user_experience, user_studies, user_supportive, user_oriented_framework, role_playing], 10).

themes2(tech, [flash, nfc, active_tokens, application_development_framework, authoring_tools, 
                             computer_vision, programming_languages, phidgets, thermochromic_displays, 
                             markup_language, smart_artifacts],                                                         9).

themes2(embodiment, [body, gesture_input, embodied_experience, embodied_interaction, embodiment, 
                                                                                sensory_mapping, somatics],             8).
themes2(mobility, [mobile_devices, mobile_phones, mobile_technology, movement_analysis, movement, 
                                                                                       kinesthetic_sense, mobility],    6).

themes2(physicality, [physical_gestures, physical_interaction, physical_interfaces, 
                                     physical_manipulatives, material_narratives, personal_objects],                    6).

themes2(use_context, [industrial_configuration, pneumatics, refrigeration_technicians, 
                         system_maintenance, work_practice, travel, digital_video_editing, multihandicapped_children],  5).

themes2(cognition, [cognitive_development, distributed_cognition, image_schemas, embodied_cognition, passive_awareness], 4).
themes2(place,      [home, domestic_technology, location_based_design, location_based_narrative, public_space],          4).
themes2(haptics,          [haptic_interface, haptic_user_interfaces, haptics, tactile_interface, tactile, touch], 6).
themes2(collaboration,    [cscw, collaboration, group_awareness, social_interaction],                             5).
themes2(consciousness,    [biofeedback, emotional_awareness, empathy, identity, intuitivity],                     4).
themes2(philosophy,       [action research, adaptability, contemplation, phenomenology],                          4).
themes2(play,             [play, game_heuristics, edutainment, interactive_toys],                                 3).
themes2(music,            [music, musical_instrument, musical_performance, sound_feedback],                       3).
themes2(ambience,         [ambient_display, ambient_environment],                                                 3).
themes2(narrative,        [material narratives, location-based narrative, reading],                               3).
themes2(intimacy,         [intimacy, intimate group communication, social intimacy],                              3).
themes2(sensing,          [sensor_network_user_interface, sensor_network, sensorial_interfaces, pen_based_input], 3).  
themes2(hci,              [HCI, interface_design],                                                                3).
themes2(communication,    [communication, multi-user communication, messaging],                                   3).
themes2(theory,           [mathematics, model, frameworks],                                                       3).
themes2(interface_locale, [tilting_table, shape_displays, visual_displays],                                       3).
themes2(fabrication,      [rapid_prototyping],                                                                    1).

themes2(arts,             [laban_effort-shape, aesthetics_artifacts, art_design_installation, 
                           choreography_of_interaction, expressiveness],                                          3).
themes2(misc,             [control_system, digitalisation, illiterate_programmer, simplicity, 
                           remote_interfaces, presentation_tool, navigable_information_space, metaphor, 
                           multi_disciplinary, real_time_behavior],                                               8).

  contributions: 
    ro: 
      title: Keynote
      authors:
        - [Tom Rodden, University of Nottingham, UK]

    bwd: 
      title: >
        .. "A Handle on What's Going On: Combining Tangible Interfaces and Ambient Displays " 
        .. "for Collaborative Groups"
      authors:
        - [Johanna Brewer,  University of California, Irvine, USA]
        - [Amanda Williams, University of California, Irvine, USA]
        - [Paul Dourish,    University of California, Irvine, USA]
      keywords: [ambient display, passive awareness, group awareness, tangible interfaces, embodied interaction]

    kmhrbrs: 
      title: "A Knife and a Cutting Board as Implicit User Interface: Towards Context-Aware Kitchen Utilities"
      authors: 
        - [Matthias Kranz,   University of Munich,           Germany]
        - [Alexis Maldonado, Technische Universität München, Germany]
        - [Benedikt Hörnler, Technische Universität München, Germany]
        - [Radu Rusu,        Technische Universität München, Germany]
        - [Michael Beetz,    Technische Universität München, Germany]
        - [Gerhard Rigoll,   Technische Universität München, Germany]
        - [Albrecht Schmidt, University of Munich,           Germany]

    vg:
      title: A Malleable Control Structure for Softwired User Interfaces
      authors:
        - [Nicolas Villar, Lancaster University, UK]
        - [Hans Gellersen, Lancaster University, UK]

    je:
      title: A Physical Approach to Tangible Interaction Design
      authors:
        - [Mads Jensen, University of Southern Denmark, Denmark]

    er:
      title: A Tangible User Interface for Multi-User Awareness Systems
      authors: 
        - [Richard Etter,  Fraunhofer IPSI, Germany]
        - [Carsten Röcker, Fraunhofer IPSI, Germany]
      keywords: [emotional awareness, music,   smart artifacts, multi-user communication, 
                 intimate group communication, tangible user interfaces, aesthetics artifacts]

    pno: 
      title: "Actuation and Tangible User Interfaces: Vaucanson duck, Robots and Shape Displays"
      authors:
        - [Ivan Poupyrev,    Sony CSL,           Japan]
        - [Tatsushi Nashida, Sony Design Center, Japan]
        - [Makoto Okabe,     Tokyo University,   Japan]
      keywords: [haptics, shape displays, interaction, collaboration]

    sh: 
      title: "Beyond video: choosing the right medium for a media rich interaction"
      authors: 
        - [Peter Shultz, Art Center College of Design, USA]

    fr:
      title: "CabBoots: Shoes with integrated Guidance System"
      authors: 
        - [Martin Frey, UdK Berlin, Germany]

    mn:
      title: Collaborative Ambient Systems by Blow Displays
      authors: 
        - [Mitsuru Minakuchi, National Institute of Information and Communications Technology, Japan]
        - [Satoshi Nakamura,  National Institute of Information and Communications Technology, Japan]
      keywords: [ambient display, haptic interface]

    hfamop:
      title: Design Research & Tangible Interaction 
      authors:
        - [Elise van den Hoven,  Eindhoven University of Technology, Netherlands]
        - [Joep Frens,           Eindhoven University of Technology, Netherlands]
        - [Dima Aliakseyeu,      Eindhoven University of Technology, Netherlands]
        - [Jean-Bernard Martens, Eindhoven University of Technology, Netherlands]
        - [Kees Overbeeke,       Eindhoven University of Technology, Netherlands]
        - [Peter Peters,         Eindhoven University of Technology, Netherlands]
      slides: https://tei.acm.org/2007/program/EliseVanDenHoven_DesignResearchAndTangibleInteraction.pdf
      keywords: [design, tangible interaction, action research, design research, 
                 embodied interaction, product design]

    hhv:
      title: "Designing for Diversity: Developing Complex Adaptive Tangible Products"
      authors:
        - [Bart Hengeveld,   University of Technology Delft,               Netherlands]
        - [Caroline Hummels, Delft University of Technology, TU Delft,     Netherlands]
        - [Riny Voort,       Viataal-Research, Development & Support, RDS, Netherlands]
      keywords: [interactive toys, adaptability, tangible interaction, 
                 multihandicapped children, complex products, edutainment]

    hr:
      title: Designing Tangible Programming Languages for Classroom Use
      authors:
        - [Michael Horn, Tufts University, USA]
        - [Robert Jacob, Tufts University, USA]
      keywords: [tangible UIs, education, children, programming languages] 

    ms:
      title: Distributed Physical Interfaces With Shared Phidgets
      authors:
        - [Nicolai Marquardt, Bauhaus-University Weimar, Germany]
        - [Saul Greenberg,    University of Calgary,     Canada]
      keywords: [distributed physical user interfaces,   phidgets]

    ma:
      title: Do tangible interfaces enhance learning?, slides]
      authors:
        - [Paul Marshall, Open University, UK]
      keywords: [tangible interface, TUI, frameworks, learning]

    slelo:
      title: Explicit interaction for surgical rehabilitation
      authors:
        - [Tomas Sokoler, K3,   Malmö University, Sweden]
        - [Jonas Löwgren,       Malmö University, Sweden]
        - [Mette Agger Eriksen, Malmö University, Sweden]
        - [Per Linde,           Malmö University, Sweden]
        - [Stefan Olofsson,     Malmö University, Sweden]
      keywords: [explicit interaction, ubiquitous computing, interaction design, use qualities]

    daw:
      title: Exploring Ambient Sound Techniques in the Design of Responsive Environments for Children
      authors:
        - [Milena Droumeva, Simon Fraser Unversity, Canada]
        - [Alissa Antle,    Simon Fraser University, Canada]
        - [Ron Wakkary,     Simon Fraser University, Canada]
      keywords: [children, sound feedback, interaction, responsive environments, 
                 participatory design, collaboration]

    ss:
      title: Freequent Traveller
      authors:
        - [Susanne Schuricht, University of the Arts Berlin, Germany]
        - [Tobias Schmidt,    University of the Arts Berlin, Germany]
      cowriters:
        - [Michael Hohl,      Sheffield Hallam University,                   UK]
        - [Mirjam Struppek,   Interactionfield, Urban Media Research Berlin, Germany]
      keywords: [interactive installation, mobility, home, identity, embodied experience, 
                 biofeedback, communication, digitalisation, travel, contemplation]

    mo:
      title: >
        .. From Hand-Held to Body-Worn: Embodied Experiences of the Design and Use 
        ..   of a Wearable Movement-Based Interaction Concept, slides 6MB]
      authors:
        - [Jin Moen, Interactive Institute; Moement R&D, Sweden]
      keywords: [movement quality, movement-based interaction, kinesthetics, 
                 wearable artifacts, embodied interaction, social context of use]

    pwa:
      title: "Gesture Connect: Facilitating Tangible Interaction With a Flick Of The Wrist"
      authors:
        - [Trevor Pering,  Intel Research,           USA]
        - [Roy Want,       Intel Research,           USA]
        - [Yaw Anokwa,     University of Washington, USA]
      keywords: [NFC, physical gestures, mobile phones, tangible interaction]

    re:
      title: Giving Materials a Voice
      authors:
        - [Hannah Regier, Art Center College of Design, USA]
      keywords: [material narratives, design process, communication design, tangible interfaces]

    hi:
      title: "Image Schemas and Their Metaphorical Extensions: Intuitive Patterns for Tangible Interaction"
      authors:
        - [Joern Hurtienne,       Technische Universität Berlin,                                         Germany]
        - [Johann Habakuk Israel, Fraunhofer-Institute for Production Systems and Design Technology IPK, Germany]
      keywords: [tangible user interfaces, intuitivity, image schemas, metaphor, embodiment]

    mo:
      title: "Keep in Touch: A Tactile-Vision Intimate Interface"
      authors:
        - [Nima Motamedi, Simon Fraser University, Canada]
      keywords: [intimacy, tactile, sensorial interfaces, sensory mapping]

    dh:
      title: Lessons from an AR Book study
      authors:
        - [Andreas Dünser, HIT Lab NZ, University of Canterbury, New Zealand]
        - [Eva Hornecker,  HIT Lab NZ, University of Canterbury, New Zealand]
      keywords: [reading, augmented reality, interactive book, children]

    sn:
      title: "PaperPoint: A Paper-Based Presentation and Interactive Paper Prototyping Toolkit"
      authors:
        - [Beat Signer,  ETH Zurich, Switzerland]
        - [Moira Norrie, ETH Zurich, Switzerland]
      keywords: [paper user interface, presentation tool, rapid prototyping, pen-based input]

    pa:
      title: >
        .. "Physical Interventions in a Location Based Cultural Narrative: "
        ..   "A Case Study of Embedded Media in Public Space Installations"
      authors:
        - [Amanda Parkes,   MIT Media Lab,             USA]
        - [Jussi Angesleva, University of Arts Berlin, Germany]
      keywords: [embedded interaction, visual displays, thermochromic displays, location-based narrative]

    snkbssap:
      title: "PillowTalk: Can We Afford Intimacy?"
      authors:
        - [Thecla Schiphorst, Simon Fraser University,              Canada]
        - [Frank Nack,        V2_ Institute for the Unstable Media, Netherlands]
        - [Michiel Kauwatjoe, V2_ Institute for the Unstable Media, Netherlands]
        - [Simon de Bakker,   V2_ Institute for the Unstable Media, Canada]
        - [Stock Stock,       V2_ Institute for the Unstable Media, Netherlands]
        - [Hielke Schut,      Eindhoven University of Technology,   Netherlands]
        - [Lora Aroyo,        Eindhoven University of Technology,   Netherlands]
        - [Angel Perez,       Eindhoven University of Technology,   Netherlands]
      keywords: [social intimacy, tactile interface, somatics, movement analysis, 
                 Laban effort-shape, tangible UIs, art/design installation, play, 
                 social interaction, user experience, ambient environment, choreography of interaction]

    kb:
      title: "reacTIVision: A Computer-Vision Framework for Table-Based Tangible Interaction"
      authors:
        - [Martin Kaltenbrunner, Universitat Pompeu Fabra, Spain]
        - [Ross Bencina,         Sonic Fritter Pty Ltd,    Australia]
      keywords: [tangible user interface, computer vision, application development framework]

    ehlo:
      title: Reclaiming Public Space - [Designing for Public Interaction with Private Devices
      authors:
        - [Eva Eriksson,            Chalmers University of Technology, Sweden]
        - [Thomas Riisgaard Hansen, University of Aarhus,              Denmark]
        - [Andreas Lykke-Olesen,    Aarhus School of Architecture,     Denmark]
      keywords: [interaction design, public space, mobile technology]

    rtsi:
      title: Remote Active Tangible Interactions
      authors:
        - [Jan Richter,    University of South Australia,            Australia]
        - [Bruce Thomas,   University of South Australia,            Australia]
        - [Maki Sugimoto,  The University of Electro-Communications, Japan]
        - [Masahiko Inami, University of Electro-Communications,     Japan]
      slides: https://tei.acm.org/2007/program/RemoteActiveTangibleInteractions.pdf
      keywords: [tangible user interfaces, evaluation, remote interfaces]

    cgz:
      title: Simplicity in Interaction Design
      authors:
        - [Angela Chang,     MIT Media Lab, USA]
        - [James Gouldstone, MIT Media Lab, USA]
        - [Jamie Zigelbaum,  MIT Media Lab, USA]
      keywords: [interface design, expressiveness, simplicity, usability]

    gthesj:
      title: "Smart Blocks: A Tangible Mathematical Manipulative"
      authors:
        - [Audrey Girouard,   Tufts University, USA]
        - [Erin Treacy,       Tufts University, USA]
        - [Leanne Hirshfield, Tufts University, USA]
        - [Stacey Ecott,      Tufts University, USA]
        - [Orit Shaer,        Tufts University, USA]
        - [Robert Jacob,      Tufts University, USA]
      keywords: [tangible user interface, education, mathematics, manipulatives]

    bi:
      title: Spatializing Real Time Interactive Environments
      authors:
        - [Nimish Biloria, TU Delft, Netherlands]
      keywords: [real-time behavior, multi-disciplinary, control system, interaction, pneumatics]

    eng:
      title: "StickySpots: Using Location to Embed Technology in the Social Practices of the Home"
      authors:
        - [Kathryn Elliot,     University of Calgary, Canada]
        - [Carman Neustaedter, University of Calgary, Canada]
        - [Saul Greenberg,     University of Calgary, Canada]
      keywords: [domestic technology, location-based design, messaging, ubiquitous computing, case studies]

    vfh:
      title: "TagTiles: optimal challenge in educational electronics"
      authors:
        - [Janneke Verhaegh, Philips Research Europe, Netherlands]
        - [Willem Fontijn,   Philips Research, Netherlands]
        - [Jettie Hoonhout,  Philips Research, Netherlands]
      keywords: [educational game, tangible interface, game heuristics]

    hn:
      title: "Tangible Image Studio: Augmented Reality Based Tangible Interface Tool for Digital Imaging"
      authors:
        - [Jung-ah Hwang, KAIST, South Korea]
        - [Tek-jin Nam,   KAIST, South Korea]

    bvhhb:
      title: "Tangible interaction in tabletop games: comparing iconic and symbolic play pieces"
      authors:
        - [Saskia Bakker,       Eindhoven University of Technology,      Netherlands]
        - [Debby Vorstenbosch,  Eindhoven University of Technology,      Netherlands]
        - [Elise van den Hoven, Eindhoven University of Technology,      Netherlands]
        - [Gerard Hollemans,    Philips Research Laboratories Eindhoven, Netherlands]
        - [Tom Bergman,         Philips Research Laboratories Eindhoven, Netherlands]

    scb:
      title: Tangible user interfaces for configuration practices
      authors:
        - [Larisa Sitorus, University of Southern Denmark, Denmark]
        - [Shan Shan Cao,  University of Southern Denmark, Denmark]
        - [Jacob Buur,     University of Southern Denmark, Denmark]
      keywords: [refrigeration technicians, industrial configuration, 
                 tangible user interface, user supportive, work practice, system maintenance]

    rhlck:
      title: Tap Input as an Embedded Interaction Method for Mobile Devices, slides]
      authors:
        - [Sami Ronkainen, Nokia, Finland]
        - [Jonna Hakkila,  Nokia, Finland]
        - [Jukka Linjama,  Nokia, Finland]
        - [Ashley Colley,  Nokia, Finland]
        - [Saana Kaleva,   Nokia, Finland]
      keywords: [gesture input, haptic user interfaces, mobile devices, user studies]

    km:
      title: "Teaching Table: A tangible mentor for pre-K math education, slides"
      authors:
        - [Madhur Khandelwal, Georgia Institute of Technology, USA]
        - [Ali Mazalek,       Georgia Institute of Technology, USA]
      keywords: [tangible computing, education, tabletop sensing, physical manipulatives, learning toys]

    db:
      title: The card box at hand
      authors:
        - [Tanja Döring,    University of Hamburg, Germany]
        - [Steffi Beckhaus, University of Hamburg, Germany]

    an:
      title: >
        .."The CTI Framework: Informing the Design of Tangible and Spatial Interactive "
        ..  "Systems for Children"
      authors:
        - [Alissa Antle, Simon Fraser University, Canada]
      keywords: [tangible interfaces, spatial interaction, embodied cognition, 
                 cognitive development, interaction design, children]

    lre:
      title: "The Feel Dimension of Technology Interaction: Exploring Tangibles through Movement and Touch"
      authors:
        - [Astrid Larssen, University of Technology Sydney, Australia]
        - [Toni Robertson, University of Technology Sydney, Australia]
        - [Jenny Edwards, University of Technology Sydney, Australia]
      keywords: [body, embodiment, interaction, interaction design, kinesthetic sense, movement, 
                 phenomenology, tangibility, touch]

    lcgs:
      title: "The Meatbook: Tangible and Visceral Interaction"
      authors:
        - [Aaron Levisohn, Simon Fraser University, Canada]
        - [Jayme Cochrane, Simon Fraser University, Canada]
        - [Diane Gromala,  Simon Fraser University, Canada]
        - [Jinsil Seo,     Simon Fraser University, Canada]

    jgka:
      title:
        "The reacTable: Exploring the Synergy between Live Music Performance and Tabletop Tangible Interfaces"
      authors:
        - [Sergi Jorda, Pompeu Fabra University, Spain]
        - [Günter Geiger, Pompeu Fabra University, Spain]
        - [Martin Kaltenbrunner, Pompeu Fabra University, Spain]
        - [Marcos Alonso, Pompeu Fabra University, Spain]
      keywords: [tangible interfaces, tabletop interfaces, musical instrument, 
                 musical performance, design, interaction techniques]

    zhsj:
      title: "The Tangible Video Editor: Collaborative Video Editing with Active Tokens"
      authors:
        - [Jamie Zigelbaum, MIT Media Lab,    USA]
        - [Michael Horn,    Tufts University, USA]
        - [Orit Shaer,      Tufts University, USA]
        - [Robert Jacob,    Tufts University, USA]
      keywords: [tangible user interface, digital video editing, active tokens,
                 interface design, CSCW, distributed cognition, tabletop interaction, 
                 physical interaction]

    lmk:
      title: "Tilting Table: A Movable Screen"
      authors:
        - [Hyun-Jean Lee,     Georgia Institute of Technology, USA]
        - [Ali Mazalek,       Georgia Institute of Technology, USA]
        - [Madhur Khandelwal, Georgia Institute of Technology, USA]
      keywords: [tangible interface, tilting table, interactive video and sound installation, 
                 navigable information space]

    mk:
      title: Towards Sensor Network User Interfaces
      authors:
        - [David Merrill,    MIT Media Laboratory, USA]
        - [Jeevan Kalanithi, MIT Media Laboratory, USA]
      keywords: [sensor network user interface (SNUI), tangible user interface (TUI), 
                 sensor network, siftable computing interface]

    sm:
      title: Using Magnets in Physical Blocks That Behave As Programming Objects
      authors:
        - [Andrew Smith, African Advanced Institute for Information & Communications Technology, South Africa]
      keywords: [TUI, digital manipulatives, Montessori-inspired manipulatives, illiterate programmer]

    mrgk:
      title: Using Personal Objects as Tangible Interfaces for Memory Recollection and Sharing
      authors:
        - [Elena Mugellini,  University of Applied Sciences of Western Switzerland, Fribourg, Switzerland]
        - [Elisa Rubegni,    University of Siena, Italy]
        - [Sandro Gerardi,   University of Applied Sciences of Western Switzerland, Fribourg, Switzerland]
        - [Omar Abou Khaled, University of Applied Sciences of Western Switzerland, Fribourg, Switzerland]
      keywords: [HCI, tangible user interface, personal objects, user-oriented framework, model, markup language]

    svgs:
      title: "VoodooFlash: Authoring across Physical and Digital Form"
      authors:
        - [Wolfgang Spiessl, University of Munich, Germany]
        - [Nicolas Villar,   Lancaster University, UK]
        - [Hans Gellersen,   Lancaster University, UK]
        - [Albrecht Schmidt, University of Munich, Germany]
      keywords: [product design, physical interfaces, authoring tools, Flash]

    bsh:
      title: When is Role Playing really experiential? Case studies
      authors:
        - [Stella Boess,     Delft University of Technology, Netherlands]
        - [Daniel Saakes,    Delft University of Technology, Netherlands]
        - [Caroline Hummels, Delft University of Technology, Netherlands]
      keywords: [role playing, design process, experience, empathy]
    
    twoMinuteMadness1: 
      eho: 
        title:   "Reclaiming Public Space: Designing for Public Interaction with Private Devices"
        authors: [Eva Eriksson, Thomas Riisgaard Hansen, Andreas Lykke-Olesen]

      lka:  
        title:   "Tilting Table: A Movable Screen"
        authors: [Hyun-Jean Lee, Madhur Khandelwal, Ali Mazalek]

      db:
        title:   >
           .."The Card Box at Hand: Exploring the Potentials of a Paper-Based Tangible Interface "
           .. "for Education and Research in Art History"
        authors:  [Tanja Döring, Steffi Beckhaus] 
        keywords: [tabletop tangible interface, paper card interface, digital art history, 
                   creativity support tool, information visualization]

      lcgs:
        title:   "The Meatbook: Tangible and Visceral Interaction"
        authors:  [Aaron Levisohn, Jayme Cochrane, Diane Gromala, Jinsil Seo]
        keywords: [Tangible interfaces for artworks, organic-inorganic interfaces]

      bvhhb: 
        title:    "Weathergods: tangible interaction in a digital tabletop game" 
        authors:  [Saskia Bakker, Debby Vorstenbosch, Elise van den Hoven, Gerard Hollemans, Tom Bergman]
        keywords: [interaction design, digital tabletop gaming, tangible user interfaces, 
                   pervasive games, tangible interaction]

      re:
        title:   Giving Materials a Voice
        authors: [Hannah Regier]

      jgak:
        title: "The reacTable: Exploring the Synergy between Live Music Performance and Tabletop Tangible Interfaces"
        authors: [Sergi Jorda, Günter Geiger, Marcos Alonso, Martin Kaltenbrunner]
        media:   [https://tei.acm.org/2007/program/JordaEtAl_Reactable.wmv]

      hj:
        title:   Designing Tangible Programming Languages for Classroom Use
        authors: [Michael Horn, Robert Jacob]

      dh:
        title:   Lessons from an AR Book study
        authors: [Andreas Dünser, Eva Hornecker]

      daw:
        title:   Exploring Ambient Sound Techniques in the Design of Responsive Environments for Children
        authors: [Milena Droumeva, Alissa Antle, Ron Wakkary]

      sc:
        title:   Freequent Traveller 
        authors: [Susanne Schuricht, Tobias Schmidt]
        media:   [http://sushu.de/free/, https://tei.acm.org/2007/program/SusanneSchuricht_FrequentTraveller.pdf]

      je:
        title:    A Physical Approach to Tangible Interaction Design
        authors:  [Mads Jensen]
        keywords: [tangible interaction, physicality, interaction qualities, physical metaphor, video action wall]

    twoMinuteMadness2:
      rtsi: 
        title:   Remote Active Tangible Interactions 
        authors: [Jan Richter, Bruce Thomas, Maki Sugimoto, Masahiko Inami]
        media:   [https://tei.acm.org/2007/program/RemoteActiveTangibleInteractions.pdf]

      kb:
        title:   "reacTIVision: A Computer-Vision Framework for Table-Based Tangible Interaction"
        authors: [Martin Kaltenbrunner, Ross Bencina]

      mkm:
        title:   "Siftables: Towards Sensor Network User Interfaces"
        authors: [David Merrill, Jeevan Kalanithi, Pattie Maes]

      vg:
        title:   A Malleable Control Structure for Softwired User Interfaces
        authors: [Nicolas Villar, Hans Gellersen]

      sm:
        title:   Using Magnets in Physical Blocks That Behave As Programming Objects
        authors: Andrew Smith

      mn:
        title:   Collaborative Ambient Systems by Blow Displays
        authors: [Mitsuru Minakuchi, Satoshi Nakamura]

      sh:
        title:    Brand consciousness as a driving design force
        authors:  Peter Shultz
        keywords: [branding, slide projectors, medium selection]

      vfh:
        title:   "TagTiles: optimal challenge in educational electronics"
        authors: [Janneke Verhaegh, Willem Fontijn, Jettie Hoonhout]

      gshesj:
        title:   "Smart Blocks: A Tangible Mathematical Manipulative"
        authors: [Audrey Girouard, Erin Treacy Solovey, Leanne Hirshfield, Stacey Ecott, Orit Shaer, Robert Jacob]

      fr:
        title:    "CabBoots: Shoes with integrated Guidance System"
        authors:  [Martin Frey]
        keywords: [human-machine interface, haptic interface, tangible interface,
                   tactile feedback, guidance system, augmented reality]

      bsh:
        title: When is Role Playing really experiential? Case studies
        authors: [Stella Boess, Daniel Saakes, Caroline Hummels]

      kmhrbrs:
        title: Context-Aware Kitchen Utilities
        authors: [Matthias Kranz, Alexis Maldonado, Benedikt Hörnler, Radu Rusu, Michael Beetz, 
                  Gerhard Rigoll, Albrecht Schmidt]

### end ###