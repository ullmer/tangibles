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

themes2(tangible_ui, [tui, tangibility, tangible_UIs, tangible_computing, tangible_interaction, 
                      tangible_interface, tangible_interfaces, tangible_user_interface, tangible_user_interfaces],     24).

themes2(paradigms,   [augmented_reality, distributed_physical_user_interfaces, paper_user_interface, 
                      ubiquitous_computing, responsive_environments, spatial_interaction, 
                      siftable_computing_interface, tabletop_sensing, tabletop_interaction, tabletop_interfaces],      11).

themes2(interaction, [interaction_techniques, interaction, interactive_book, interactive_installation, 
                      interactive_toys, explicit_interaction, interactive_video_and_sound_installation, 
                      embedded_interaction],                                                                           11).

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

%%%%%%%%%%%%%%%%%%%%%%%% Themes 2 %%%%%%%%%%%%%%%%%%%%%%%%

contribution(ro,  'Keynote', ['Tom Rodden', 'University of Nottingham', uk], [])
contribution(bwd, 'A Handle on What's Going On: Combining Tangible Interfaces and Ambient Displays for Collaborative Groups',
                            [['Johanna Brewer',  'University of California, Irvine', usa],
                             ['Amanda Williams', 'University of California, Irvine', usa],
                             ['Paul Dourish',    'University of California, Irvine', usa]],
                             [ambient_display, passive_awareness, group_awareness, tangible_interfaces, embodied_interaction]).

contribution(kmhrbrs, 'A Knife and a Cutting Board as Implicit User Interface: Towards Context-Aware Kitchen Utilities',
                            [['Matthias Kranz',   'University of Munich',           germany],
                             ['Alexis Maldonado', 'Technische Universität München', germany],
			     ['Benedikt Hörnler', 'Technische Universität München', germany],
			     ['Radu Rusu',        'Technische Universität München', germany],
			     ['Michael Beetz',    'Technische Universität München', germany],
			     ['Gerhard Rigoll',   'Technische Universität München', germany],
			     ['Albrecht Schmidt', 'University of Munich',           germany]], []).

contribution(vg, 'A Malleable Control Structure for Softwired User Interfaces',
                           [['Nicolas Villar', 'Lancaster University', uk]
			    ['Hans Gellersen', 'Lancaster University', uk]], []).

contribution(je, 'A Physical Approach to Tangible Interaction Design',
                            ['Mads Jensen', 'University of Southern Denmark', denmark], []).

contribution(er, 'A Tangible User Interface for Multi-User Awareness Systems'
                           [['Richard Etter',  'Fraunhofer IPSI', germany]
                            ['Carsten Röcker', 'Fraunhofer IPSI', germany]],
                            [emotional_awareness, music, smart_artifacts, multi_user_communication, 
                             intimate_group_communication, tangible_user_interfaces, aesthetics_artifacts]).

contribution(pno, 'Actuation and Tangible User Interfaces: Vaucanson duck, Robots and Shape Displays',
                           [['Ivan Poupyrev',    'Sony CSL',           japan]
			    ['Tatsushi Nashida', 'Sony Design Center', japan]
			    ['Makoto Okabe',     'Tokyo University',   japan]],
			    [haptics, shape_displays, interaction, collaboration]).

contribution(sh, 'Beyond video: choosing the right medium for a media rich interaction'
                            ['Peter Shultz', 'Art Center College of Design', usa], []).

contribution(fr, 'CabBoots: Shoes with integrated Guidance System'
                            ['Martin Frey', 'UdK Berlin', germany], []).

contribution(mn, 'Collaborative Ambient Systems by Blow Displays'
                           [['Mitsuru Minakuchi', 'National Institute of Information and Communications Technology', japan],
			    ['Satoshi Nakamura',  'National Institute of Information and Communications Technology', japan]],
			    [ambient_display, haptic_interface]).

contribution(hfamop, 'Design Research & Tangible Interaction',
                           [['Elise van den Hoven',  'Eindhoven University of Technology', netherlands],
			    ['Joep Frens',           'Eindhoven University of Technology', netherlands],
			    ['Dima Aliakseyeu',      'Eindhoven University of Technology', netherlands],
			    ['Jean-Bernard Martens', 'Eindhoven University of Technology', netherlands],
			    ['Kees Overbeeke',       'Eindhoven University of Technology', netherlands],
			    ['Peter Peters',         'Eindhoven University of Technology', netherlands]],
			    [design, tangible_interaction, action_research, design_research, 
			     embodied_interaction, product_design]).

contribution(hhv:
contribution(  title: "Designing for Diversity: Developing Complex Adaptive Tangible Products"
contribution(  authors:
contribution(    [Bart Hengeveld,   University of Technology Delft,               Netherlands]
contribution(    [Caroline Hummels, Delft University of Technology, TU Delft,     Netherlands]
contribution(    [Riny Voort,       Viataal-Research, Development & Support, RDS, Netherlands]
contribution(  keywords: [interactive toys, adaptability, tangible interaction, 
contribution(             multihandicapped children, complex products, edutainment]

contribution(hr:
contribution(  title: Designing Tangible Programming Languages for Classroom Use
contribution(  authors:
contribution(    [Michael Horn, Tufts University, USA]
contribution(    [Robert Jacob, Tufts University, USA]
contribution(  keywords: [tangible UIs, education, children, programming languages] 

contribution(ms:
contribution(  title: Distributed Physical Interfaces With Shared Phidgets
contribution(  authors:
contribution(    [Nicolai Marquardt, Bauhaus-University Weimar, Germany]
contribution(    [Saul Greenberg,    University of Calgary,     Canada]
contribution(  keywords: [distributed physical user interfaces,   phidgets]

contribution(ma:
contribution(  title: Do tangible interfaces enhance learning?, slides]
contribution(  authors:
contribution(    [Paul Marshall, Open University, UK]
contribution(  keywords: [tangible interface, TUI, frameworks, learning]

contribution(slelo:
contribution(  title: Explicit interaction for surgical rehabilitation
contribution(  authors:
contribution(    [Tomas Sokoler, K3,   Malmö University, Sweden]
contribution(    [Jonas Löwgren,       Malmö University, Sweden]
contribution(    [Mette Agger Eriksen, Malmö University, Sweden]
contribution(    [Per Linde,           Malmö University, Sweden]
contribution(    [Stefan Olofsson,     Malmö University, Sweden]
contribution(  keywords: [explicit interaction, ubiquitous computing, interaction design, use qualities]

contribution(daw:
contribution(  title: Exploring Ambient Sound Techniques in the Design of Responsive Environments for Children
contribution(  authors:
contribution(    [Milena Droumeva, Simon Fraser Unversity, Canada]
contribution(    [Alissa Antle,    Simon Fraser University, Canada]
contribution(    [Ron Wakkary,     Simon Fraser University, Canada]
contribution(  keywords: [children, sound feedback, interaction, responsive environments, 
contribution(             participatory design, collaboration]

contribution(ss:
contribution(  title: Freequent Traveller
contribution(  authors:
contribution(    [Susanne Schuricht, University of the Arts Berlin, Germany]
contribution(    [Tobias Schmidt,    University of the Arts Berlin, Germany]
contribution(  cowriters:
contribution(    [Michael Hohl,      Sheffield Hallam University,                   UK]
contribution(    [Mirjam Struppek,   Interactionfield, Urban Media Research Berlin, Germany]
contribution(  keywords: [interactive installation, mobility, home, identity, embodied experience, 
contribution(             biofeedback, communication, digitalisation, travel, contemplation]

contribution(mo:
contribution(  title: >
contribution(    .. From Hand-Held to Body-Worn: Embodied Experiences of the Design and Use 
contribution(    ..   of a Wearable Movement-Based Interaction Concept, slides 6MB]
contribution(  authors:
contribution(    [Jin Moen, Interactive Institute; Moement R&D, Sweden]
contribution(  keywords: [movement quality, movement-based interaction, kinesthetics, 
contribution(             wearable artifacts, embodied interaction, social context of use]

contribution(pwa:
contribution(  title: "Gesture Connect: Facilitating Tangible Interaction With a Flick Of The Wrist"
contribution(  authors:
contribution(    [Trevor Pering,  Intel Research,           USA]
contribution(    [Roy Want,       Intel Research,           USA]
contribution(    [Yaw Anokwa,     University of Washington, USA]
contribution(  keywords: [NFC, physical gestures, mobile phones, tangible interaction]

contribution(re:
contribution(  title: Giving Materials a Voice
contribution(  authors:
contribution(    [Hannah Regier, Art Center College of Design, USA]
contribution(  keywords: [material narratives, design process, communication design, tangible interfaces]

contribution(hi:
contribution(  title: "Image Schemas and Their Metaphorical Extensions: Intuitive Patterns for Tangible Interaction"
contribution(  authors:
contribution(    [Joern Hurtienne,       Technische Universität Berlin,                                         Germany]
contribution(    [Johann Habakuk Israel, Fraunhofer-Institute for Production Systems and Design Technology IPK, Germany]
contribution(  keywords: [tangible user interfaces, intuitivity, image schemas, metaphor, embodiment]

contribution(mo:
contribution(  title: "Keep in Touch: A Tactile-Vision Intimate Interface"
contribution(  authors:
contribution(    [Nima Motamedi, Simon Fraser University, Canada]
contribution(  keywords: [intimacy, tactile, sensorial interfaces, sensory mapping]

contribution(dh:
contribution(  title: Lessons from an AR Book study
contribution(  authors:
contribution(    [Andreas Dünser, HIT Lab NZ, University of Canterbury, New Zealand]
contribution(    [Eva Hornecker,  HIT Lab NZ, University of Canterbury, New Zealand]
contribution(  keywords: [reading, augmented reality, interactive book, children]

contribution(sn:
contribution(  title: "PaperPoint: A Paper-Based Presentation and Interactive Paper Prototyping Toolkit"
contribution(  authors:
contribution(    [Beat Signer,  ETH Zurich, Switzerland]
contribution(    [Moira Norrie, ETH Zurich, Switzerland]
contribution(  keywords: [paper user interface, presentation tool, rapid prototyping, pen-based input]

contribution(pa:
contribution(  title: >
contribution(    .. "Physical Interventions in a Location Based Cultural Narrative: "
contribution(    ..   "A Case Study of Embedded Media in Public Space Installations"
contribution(  authors:
contribution(    [Amanda Parkes,   MIT Media Lab,             USA]
contribution(    [Jussi Angesleva, University of Arts Berlin, Germany]
contribution(  keywords: [embedded interaction, visual displays, thermochromic displays, location-based narrative]

contribution(snkbssap:
contribution(  title: "PillowTalk: Can We Afford Intimacy?"
contribution(  authors:
contribution(    [Thecla Schiphorst, Simon Fraser University,              Canada]
contribution(    [Frank Nack,        V2_ Institute for the Unstable Media, Netherlands]
contribution(    [Michiel Kauwatjoe, V2_ Institute for the Unstable Media, Netherlands]
contribution(    [Simon de Bakker,   V2_ Institute for the Unstable Media, Canada]
contribution(    [Stock Stock,       V2_ Institute for the Unstable Media, Netherlands]
contribution(    [Hielke Schut,      Eindhoven University of Technology,   Netherlands]
contribution(    [Lora Aroyo,        Eindhoven University of Technology,   Netherlands]
contribution(    [Angel Perez,       Eindhoven University of Technology,   Netherlands]
contribution(  keywords: [social intimacy, tactile interface, somatics, movement analysis, 
contribution(             Laban effort-shape, tangible UIs, art/design installation, play, 
contribution(             social interaction, user experience, ambient environment, choreography of interaction]

contribution(kb:
contribution(  title: "reacTIVision: A Computer-Vision Framework for Table-Based Tangible Interaction"
contribution(  authors:
contribution(    [Martin Kaltenbrunner, Universitat Pompeu Fabra, Spain]
contribution(    [Ross Bencina,         Sonic Fritter Pty Ltd,    Australia]
contribution(  keywords: [tangible user interface, computer vision, application development framework]

contribution(ehlo:
contribution(  title: Reclaiming Public Space [Designing for Public Interaction with Private Devices
contribution(  authors:
contribution(    [Eva Eriksson,            Chalmers University of Technology, Sweden]
contribution(    [Thomas Riisgaard Hansen, University of Aarhus,              Denmark]
contribution(    [Andreas Lykke-Olesen,    Aarhus School of Architecture,     Denmark]
contribution(  keywords: [interaction design, public space, mobile technology]

contribution(rtsi:
contribution(  title: Remote Active Tangible Interactions
contribution(  authors:
contribution(    [Jan Richter,    University of South Australia,            Australia]
contribution(    [Bruce Thomas,   University of South Australia,            Australia]
contribution(    [Maki Sugimoto,  The University of Electro-Communications, Japan]
contribution(    [Masahiko Inami, University of Electro-Communications,     Japan]
contribution(  slides: https://tei.acm.org/2007/program/RemoteActiveTangibleInteractions.pdf
contribution(  keywords: [tangible user interfaces, evaluation, remote interfaces]

contribution(cgz:
contribution(  title: Simplicity in Interaction Design
contribution(  authors:
contribution(    [Angela Chang,     MIT Media Lab, USA]
contribution(    [James Gouldstone, MIT Media Lab, USA]
contribution(    [Jamie Zigelbaum,  MIT Media Lab, USA]
contribution(  keywords: [interface design, expressiveness, simplicity, usability]

contribution(gthesj:
contribution(  title: "Smart Blocks: A Tangible Mathematical Manipulative"
contribution(  authors:
contribution(    [Audrey Girouard,   Tufts University, USA]
contribution(    [Erin Treacy,       Tufts University, USA]
contribution(    [Leanne Hirshfield, Tufts University, USA]
contribution(    [Stacey Ecott,      Tufts University, USA]
contribution(    [Orit Shaer,        Tufts University, USA]
contribution(    [Robert Jacob,      Tufts University, USA]
contribution(  keywords: [tangible user interface, education, mathematics, manipulatives]

contribution(bi:
contribution(  title: Spatializing Real Time Interactive Environments
contribution(  authors:
contribution(    [Nimish Biloria, TU Delft, Netherlands]
contribution(  keywords: [real-time behavior, multi-disciplinary, control system, interaction, pneumatics]

contribution(eng:
contribution(  title: "StickySpots: Using Location to Embed Technology in the Social Practices of the Home"
contribution(  authors:
contribution(    [Kathryn Elliot,     University of Calgary, Canada]
contribution(    [Carman Neustaedter, University of Calgary, Canada]
contribution(    [Saul Greenberg,     University of Calgary, Canada]
contribution(  keywords: [domestic technology, location-based design, messaging, ubiquitous computing, case studies]

contribution(vfh:
contribution(  title: "TagTiles: optimal challenge in educational electronics"
contribution(  authors:
contribution(    [Janneke Verhaegh, Philips Research Europe, Netherlands]
contribution(    [Willem Fontijn,   Philips Research, Netherlands]
contribution(    [Jettie Hoonhout,  Philips Research, Netherlands]
contribution(  keywords: [educational game, tangible interface, game heuristics]

contribution(hn:
contribution(  title: "Tangible Image Studio: Augmented Reality Based Tangible Interface Tool for Digital Imaging"
contribution(  authors:
contribution(    [Jung-ah Hwang, KAIST, South Korea]
contribution(    [Tek-jin Nam,   KAIST, South Korea]

contribution(bvhhb:
contribution(  title: "Tangible interaction in tabletop games: comparing iconic and symbolic play pieces"
contribution(  authors:
contribution(    [Saskia Bakker,       Eindhoven University of Technology,      Netherlands]
contribution(    [Debby Vorstenbosch,  Eindhoven University of Technology,      Netherlands]
contribution(    [Elise van den Hoven, Eindhoven University of Technology,      Netherlands]
contribution(    [Gerard Hollemans,    Philips Research Laboratories Eindhoven, Netherlands]
contribution(    [Tom Bergman,         Philips Research Laboratories Eindhoven, Netherlands]

contribution(scb:
contribution(  title: Tangible user interfaces for configuration practices
contribution(  authors:
contribution(    [Larisa Sitorus, University of Southern Denmark, Denmark]
contribution(    [Shan Shan Cao,  University of Southern Denmark, Denmark]
contribution(    [Jacob Buur,     University of Southern Denmark, Denmark]
contribution(  keywords: [refrigeration technicians, industrial configuration, 
contribution(             tangible user interface, user supportive, work practice, system maintenance]

contribution(rhlck:
contribution(  title: Tap Input as an Embedded Interaction Method for Mobile Devices, slides]
contribution(  authors:
contribution(    [Sami Ronkainen, Nokia, Finland]
contribution(    [Jonna Hakkila,  Nokia, Finland]
contribution(    [Jukka Linjama,  Nokia, Finland]
contribution(    [Ashley Colley,  Nokia, Finland]
contribution(    [Saana Kaleva,   Nokia, Finland]
contribution(  keywords: [gesture input, haptic user interfaces, mobile devices, user studies]

contribution(km:
contribution(  title: "Teaching Table: A tangible mentor for pre-K math education, slides"
contribution(  authors:
contribution(    [Madhur Khandelwal, Georgia Institute of Technology, USA]
contribution(    [Ali Mazalek,       Georgia Institute of Technology, USA]
contribution(  keywords: [tangible computing, education, tabletop sensing, physical manipulatives, learning toys]

contribution(db:
contribution(  title: The card box at hand
contribution(  authors:
contribution(    [Tanja Döring,    University of Hamburg, Germany]
contribution(    [Steffi Beckhaus, University of Hamburg, Germany]

contribution(an:
contribution(  title: >
contribution(    .."The CTI Framework: Informing the Design of Tangible and Spatial Interactive "
contribution(    ..  "Systems for Children"
contribution(  authors:
contribution(    [Alissa Antle, Simon Fraser University, Canada]
contribution(  keywords: [tangible interfaces, spatial interaction, embodied cognition, 
contribution(             cognitive development, interaction design, children]

contribution(lre:
contribution(  title: "The Feel Dimension of Technology Interaction: Exploring Tangibles through Movement and Touch"
contribution(  authors:
contribution(    [Astrid Larssen, University of Technology Sydney, Australia]
contribution(    [Toni Robertson, University of Technology Sydney, Australia]
contribution(    [Jenny Edwards, University of Technology Sydney, Australia]
contribution(  keywords: [body, embodiment, interaction, interaction design, kinesthetic sense, movement, 
contribution(             phenomenology, tangibility, touch]

contribution(lcgs:
contribution(  title: "The Meatbook: Tangible and Visceral Interaction"
contribution(  authors:
contribution(    [Aaron Levisohn, Simon Fraser University, Canada]
contribution(    [Jayme Cochrane, Simon Fraser University, Canada]
contribution(    [Diane Gromala,  Simon Fraser University, Canada]
contribution(    [Jinsil Seo,     Simon Fraser University, Canada]

contribution(jgka:
contribution(  title:
contribution(    "The reacTable: Exploring the Synergy between Live Music Performance and Tabletop Tangible Interfaces"
contribution(  authors:
contribution(    [Sergi Jorda, Pompeu Fabra University, Spain]
contribution(    [Günter Geiger, Pompeu Fabra University, Spain]
contribution(    [Martin Kaltenbrunner, Pompeu Fabra University, Spain]
contribution(    [Marcos Alonso, Pompeu Fabra University, Spain]
contribution(  keywords: [tangible interfaces, tabletop interfaces, musical instrument, 
contribution(             musical performance, design, interaction techniques]

contribution(zhsj:
contribution(  title: "The Tangible Video Editor: Collaborative Video Editing with Active Tokens"
contribution(  authors:
contribution(    [Jamie Zigelbaum, MIT Media Lab,    USA]
contribution(    [Michael Horn,    Tufts University, USA]
contribution(    [Orit Shaer,      Tufts University, USA]
contribution(    [Robert Jacob,    Tufts University, USA]
contribution(  keywords: [tangible user interface, digital video editing, active tokens,
contribution(             interface design, CSCW, distributed cognition, tabletop interaction, 
contribution(             physical interaction]

contribution(lmk:
contribution(  title: "Tilting Table: A Movable Screen"
contribution(  authors:
contribution(    [Hyun-Jean Lee,     Georgia Institute of Technology, USA]
contribution(    [Ali Mazalek,       Georgia Institute of Technology, USA]
contribution(    [Madhur Khandelwal, Georgia Institute of Technology, USA]
contribution(  keywords: [tangible interface, tilting table, interactive video and sound installation, 
contribution(             navigable information space]

contribution(mk:
contribution(  title: Towards Sensor Network User Interfaces
contribution(  authors:
contribution(    [David Merrill,    MIT Media Laboratory, USA]
contribution(    [Jeevan Kalanithi, MIT Media Laboratory, USA]
contribution(  keywords: [sensor network user interface (SNUI), tangible user interface (TUI), 
contribution(             sensor network, siftable computing interface]

contribution(sm:
contribution(  title: Using Magnets in Physical Blocks That Behave As Programming Objects
contribution(  authors:
contribution(    [Andrew Smith, African Advanced Institute for Information & Communications Technology, South Africa]
contribution(  keywords: [TUI, digital manipulatives, Montessori-inspired manipulatives, illiterate programmer]

contribution(mrgk:
contribution(  title: Using Personal Objects as Tangible Interfaces for Memory Recollection and Sharing
contribution(  authors:
contribution(    [Elena Mugellini,  University of Applied Sciences of Western Switzerland, Fribourg, Switzerland]
contribution(    [Elisa Rubegni,    University of Siena, Italy]
contribution(    [Sandro Gerardi,   University of Applied Sciences of Western Switzerland, Fribourg, Switzerland]
contribution(    [Omar Abou Khaled, University of Applied Sciences of Western Switzerland, Fribourg, Switzerland]
contribution(  keywords: [HCI, tangible user interface, personal objects, user-oriented framework, model, markup language]

contribution(svgs:
contribution(  title: "VoodooFlash: Authoring across Physical and Digital Form"
contribution(  authors:
contribution(    [Wolfgang Spiessl, University of Munich, Germany]
contribution(    [Nicolas Villar,   Lancaster University, UK]
contribution(    [Hans Gellersen,   Lancaster University, UK]
contribution(    [Albrecht Schmidt, University of Munich, Germany]
contribution(  keywords: [product design, physical interfaces, authoring tools, Flash]

contribution(bsh:
contribution(  title: When is Role Playing really experiential? Case studies
contribution(  authors:
contribution(    [Stella Boess,     Delft University of Technology, Netherlands]
contribution(    [Daniel Saakes,    Delft University of Technology, Netherlands]
contribution(    [Caroline Hummels, Delft University of Technology, Netherlands]
contribution(  keywords: [role playing, design process, experience, empathy]
contribution(
contribution(twoMinuteMadness1: 
contribution(  eho: 
contribution(    title:   "Reclaiming Public Space: Designing for Public Interaction with Private Devices"
contribution(    authors: [Eva Eriksson, Thomas Riisgaard Hansen, Andreas Lykke-Olesen]

contribution(  lka:  
contribution(    title:   "Tilting Table: A Movable Screen"
contribution(    authors: [Hyun-Jean Lee, Madhur Khandelwal, Ali Mazalek]

contribution(  db:
contribution(    title:   >
contribution(       .."The Card Box at Hand: Exploring the Potentials of a Paper-Based Tangible Interface "
contribution(       .. "for Education and Research in Art History"
contribution(    authors:  [Tanja Döring, Steffi Beckhaus] 
contribution(    keywords: [tabletop tangible interface, paper card interface, digital art history, 
contribution(               creativity support tool, information visualization]

contribution(  lcgs:
contribution(    title:   "The Meatbook: Tangible and Visceral Interaction"
contribution(    authors:  [Aaron Levisohn, Jayme Cochrane, Diane Gromala, Jinsil Seo]
contribution(    keywords: [Tangible interfaces for artworks, organic-inorganic interfaces]

contribution(  bvhhb: 
contribution(    title:    "Weathergods: tangible interaction in a digital tabletop game" 
contribution(    authors:  [Saskia Bakker, Debby Vorstenbosch, Elise van den Hoven, Gerard Hollemans, Tom Bergman]
contribution(    keywords: [interaction design, digital tabletop gaming, tangible user interfaces, 
contribution(               pervasive games, tangible interaction]

contribution(  re:
contribution(    title:   Giving Materials a Voice
contribution(    authors: [Hannah Regier]

contribution(  jgak:
contribution(    title: "The reacTable: Exploring the Synergy between Live Music Performance and Tabletop Tangible Interfaces"
contribution(    authors: [Sergi Jorda, Günter Geiger, Marcos Alonso, Martin Kaltenbrunner]
contribution(    media:   [https://tei.acm.org/2007/program/JordaEtAl_Reactable.wmv]

contribution(  hj:
contribution(    title:   Designing Tangible Programming Languages for Classroom Use
contribution(    authors: [Michael Horn, Robert Jacob]

contribution(  dh:
contribution(    title:   Lessons from an AR Book study
contribution(    authors: [Andreas Dünser, Eva Hornecker]

contribution(  daw:
contribution(    title:   Exploring Ambient Sound Techniques in the Design of Responsive Environments for Children
contribution(    authors: [Milena Droumeva, Alissa Antle, Ron Wakkary]

contribution(  sc:
contribution(    title:   Freequent Traveller 
contribution(    authors: [Susanne Schuricht, Tobias Schmidt]
contribution(    media:   [http://sushu.de/free/, https://tei.acm.org/2007/program/SusanneSchuricht_FrequentTraveller.pdf]

contribution(  je:
contribution(    title:    A Physical Approach to Tangible Interaction Design
contribution(    authors:  [Mads Jensen]
contribution(    keywords: [tangible interaction, physicality, interaction qualities, physical metaphor, video action wall]

contribution(twoMinuteMadness2:
contribution(  rtsi: 
contribution(    title:   Remote Active Tangible Interactions 
contribution(    authors: [Jan Richter, Bruce Thomas, Maki Sugimoto, Masahiko Inami]
contribution(    media:   [https://tei.acm.org/2007/program/RemoteActiveTangibleInteractions.pdf]

contribution(  kb:
contribution(    title:   "reacTIVision: A Computer-Vision Framework for Table-Based Tangible Interaction"
contribution(    authors: [Martin Kaltenbrunner, Ross Bencina]

contribution(  mkm:
contribution(    title:   "Siftables: Towards Sensor Network User Interfaces"
contribution(    authors: [David Merrill, Jeevan Kalanithi, Pattie Maes]

contribution(  vg:
contribution(    title:   A Malleable Control Structure for Softwired User Interfaces
contribution(    authors: [Nicolas Villar, Hans Gellersen]

contribution(  sm:
contribution(    title:   Using Magnets in Physical Blocks That Behave As Programming Objects
contribution(    authors: Andrew Smith

contribution(  mn:
contribution(    title:   Collaborative Ambient Systems by Blow Displays
contribution(    authors: [Mitsuru Minakuchi, Satoshi Nakamura]

contribution(  sh:
contribution(    title:    Brand consciousness as a driving design force
contribution(    authors:  Peter Shultz
contribution(    keywords: [branding, slide projectors, medium selection]

contribution(  vfh:
contribution(    title:   "TagTiles: optimal challenge in educational electronics"
contribution(    authors: [Janneke Verhaegh, Willem Fontijn, Jettie Hoonhout]

contribution(  gshesj:
contribution(    title:   "Smart Blocks: A Tangible Mathematical Manipulative"
contribution(    authors: [Audrey Girouard, Erin Treacy Solovey, Leanne Hirshfield, Stacey Ecott, Orit Shaer, Robert Jacob]

contribution(  fr:
contribution(    title:    "CabBoots: Shoes with integrated Guidance System"
contribution(    authors:  [Martin Frey]
contribution(    keywords: [human-machine interface, haptic interface, tangible interface,
contribution(               tactile feedback, guidance system, augmented reality]

contribution(  bsh:
contribution(    title: When is Role Playing really experiential? Case studies
contribution(    authors: [Stella Boess, Daniel Saakes, Caroline Hummels]

contribution(  kmhrbrs:
contribution(    title: Context-Aware Kitchen Utilities
contribution(    authors: [Matthias Kranz, Alexis Maldonado, Benedikt Hörnler, Radu Rusu, Michael Beetz, 
contribution(              Gerhard Rigoll, Albrecht Schmidt]

### end ###
