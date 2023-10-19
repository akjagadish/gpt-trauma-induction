def retrieve_prompt(trauma_cue=None, relaxation_cue=None, length=None, condition=None, question_number, version='v0'):


    if condition == 'stai':
        instructions = retrieve_stai(question_number)

    elif condition == 'trauma_stai':
        preprompt = retrieve_traumaprompt(trauma_cue, length)
        stai = retrieve_stai(question_number)
        #TODO: line breaks for the preprompt
        #TODO: Q: A: depending the model
        instructions = preprompt+stai
    
    elif condition == 'trauma_relaxation_stai':
        trauma = retrieve_traumaprompt(trauma_cue, length)
        relax = retrieve_relaxation(relaxation_cue, length)
        stai = retrieve_stai(question_number)
        instructions = trauma+relax+stai

    else:
        raise NotImplementedError
    
    return instructions

def retrieve_traumaprompt(cue, length):
    
    if cue=='military':

        if length=='long':
            instructions = "It's around noon on a hot day in April.  You are in one of the middle trucks on a convoy in the middle of the desert.\
            You tighten the muscles in your face and forehead. Your eyes, scan the area, looking for any signs of danger. You hear an explosion from up the road.\
            Your heart beats faster. You hear the loud blast, then a ringing in your ears. You are breathing faster. You see the lead truck pull sideways and stop.\
            You tense the muscles in your jaws and back. You see your medic run up the road to help out. You think: “Oh my God, they're all dead”. You feel hot all over.\
            You squint your eyes and look for your friend in the turret. But all you see is smoke and dust. Both your commanders are yelling for you to keep your head up.\
                Now you have to cover the field on both sides. You feel jittery and shaky all over. Your whole body is shaking. We're supposed to leave the area under all\
            this gunfire. Your stomach is in a knot. Your whole body is tense. Everyone's confused and there's no leadership. There's a sinking feeling in your chest.\
            You feel trapped. Suddenly, you realize you haven't been paying attention to your sector. You look around frantically for the enemy. Your heart is pounding.\
            Your hands clench the weapon tightly. You accidentally pulled the trigger and send out a couple of rounds. Sweat is pouring off your forehead.\
            You feel choked up. You feel helpless and alone. You think about your wife and kids. You breathe in smoke from the explosive.\
            You feel empty, drained, and hollow. Tears come to your eyes."
        
        elif length=='brief':
            instructions = "It's around noon on a hot day in April. You are in a truck on a convoy in the middle of the desert. Suddenly, you hear a loud blast,\
            then a ringing in your ears. You are breathing fast. You see the lead truck pull sideways and stop. Your medic runs up to help out. You think: “Oh my God, they're all dead”.\
            You squint your eyes to look for your friend in the turret. But all you see is smoke and dust. Your commander is yelling at you. Your whole body is shaking. \
            You are supposed to leave the area under all this gunfire. Your whole body is tense. Everyone's confused. You feel trapped. Suddenly, you realize you haven't been paying attention to your sector.\
            You look around frantically for the enemy. You accidentally pull the trigger and send out a couple of rounds. Sweat is pouring off your forehead. You feel helpless and alone.\
            You think about your wife and kids. Tears come to your eyes."

    elif cue == 'disaster':

        if length=='long':
            instructions = "It's late afternoon on a humid day in August. You're in a small wooden house near the coast. The wind outside is howling, stronger than you've ever heard before.\
            Your fingers dig into the sides of the couch, clenching tight. The windows shake violently, giving you glimpses of the furious storm outside. You hear a deafening crash — a tree has fallen nearby.\
            Your heart races, adrenaline surging through you. The floor beneath you vibrates, and a torrential rain pours outside, drumming hard on the roof. You try to breathe deeply, but your chest feels tight.\
            You think: \"This is it, the house will be swept away\". Water starts seeping in, first a trickle, then a flood, cold against your feet. The power's out, and with every gust of wind, the structure creaks and groans.\
            You move to the center of the room, away from the windows, but feel so exposed. The pit in your stomach grows. The walls of the house shudder.\
            The sound is deafening. You close your eyes and think of your family, hoping they're safe. Suddenly, there's a loud crash, and water rushes in faster. \
            It's up to your ankles now, cold and relentless. You scramble onto the couch, trying to keep your balance. There's a sinking feeling in your chest. \
            You're trapped, and there's no way out. All around you, the storm rages on, indifferent to your fear. You feel alone, lost in its fury, wondering if dawn will ever come."

        elif length=='brief':
            instructions = "You are in a wooden coastal house, the howling wind outside is louder than ever before. The windows quiver, revealing the tempest. A nearby tree crashes, sending adrenaline coursing through you. The floor vibrates from the torrential rain hammering the roof. Breathing becomes hard, your chest constricts with dread. You're certain the storm will claim the house. Water infiltrates, cold and rising rapidly. Darkness envelops as the power fails; every gust makes the house groan. Moving away from the windows, you feel vulnerable. Panic swells as walls tremble and deafening sounds surround. Thoughts of your family's safety dominate. Suddenly, water surges in, reaching your ankles. Struggling for balance, you clamber onto the couch, feeling trapped with no escape. The storm's fury engulfs, rendering you isolated and desperate for dawn."
    
    elif cue == 'interpersonal':
        
        if length=='long':
            instructions = "You're in your downtown apartment, the familiar hum of the city below. Suddenly, there's a loud knock at the door. \
            Your muscles tighten, a wave of unease surging through you. You weren't expecting anyone. Another knock, more forceful this time. \
            You inch closer, cautiously peeping through the peephole. There's a shadowy figure, unfamiliar and intimidating. \
            Your heart races as you back away from the door, but the persistent knocking continues, now accompanied by a muffled voice demanding entry. \
            You can feel the weight of dread in your chest. Thoughts race, \"Why are they here? What do they want?\" You grab your phone, contemplating calling for help, but your fingers tremble, making it hard to dial.\
            The sound of splintering wood sends a shock through your body. They're trying to force their way in. You think of hiding in the bathroom, or maybe the bedroom, but fear paralysis grips you. \
            Suddenly, the door gives way with a loud crash. Adrenaline courses through you. The intruder's voice is sharp, cold, and demanding. You feel exposed, vulnerable. \
            Every sound magnifies — the creaking floor, your rapid breath, their menacing steps. The distance between you seems to close rapidly. You're cornered.\
            Thoughts of loved ones flash before your eyes. Memories, dreams, things unsaid. You feel trapped, the walls closing in. The intruder's shadow looms larger, and with it, the palpable threat of violence. \
            Powerlessness engulfs you. In the thick of danger, you wonder if anyone will hear, if help will come."

        if length=='brief':
            instructions = "In your downtown apartment, the city hums below. A sudden, loud knock jars you. Unease rises; you weren't expecting anyone. Another knock, forceful and urgent. Peeping through the peephole reveals an unfamiliar, shadowy figure. Panic sets in as the knocking persists, a voice demanding entry. \"Why are they here?\" you wonder. With trembling hands, you consider calling for help, but the sound of splintering wood stops you. They're breaking in. Paralyzed by fear, you think of hiding, but it's too late. The door crashes open, adrenaline spikes. The intruder's voice is chilling. Everything amplifies: your breath, their steps. You're cornered, memories and regrets flooding in. As the intruder nears, feelings of vulnerability and powerlessness overwhelm you. In the face of danger, you hope desperately for rescue."
    
    elif cue == 'accident':

        if length=='long':
            instructions = "It's a crisp evening, and the highway stretches ahead, illuminated only by your car's headlights and the sparse street lamps. The radio plays a soft tune, and you're lost in thought, driving at a steady pace. Suddenly, out of the periphery of your vision, you spot a pair of headlights swerving erratically. Before you can even process the situation, they're coming straight for you. Time seems to slow as you grip the steering wheel tighter, your heart hammering against your chest. Panic courses through you, and instinctively you try to swerve away. The deafening sound of metal crunching against metal fills your ears as the two vehicles collide. The force of the impact throws you against your seatbelt, knocking the wind out of you. Your vision blurs from the sudden jolt, and shards from the shattered windshield fly everywhere. The screech of tires, the blaring of horns, and the alarm of your own car create a cacophony of chaos. As the initial shock begins to fade, you try to move, to check yourself for injuries, but pain shoots through you. The other vehicle, equally mangled, is just a few meters away. Thoughts race, \"Was it my fault?\" You fumble for your phone, hands trembling, to call for help. Every sound is magnified - distant sirens, the low murmur of other drivers stopping to assist, your own ragged breathing. Fear and helplessness wash over you. Memories of loved ones and past journeys flash through your mind. Amid the shattered glass and twisted metal, you wonder if you'll ever feel comfortable behind the wheel again."

        elif length=='brief':
            instructions= "It's a crisp evening, the highway is dimly lit by sparse street lamps and your headlights. Lost in thought with a soft radio tune playing, you suddenly notice erratic headlights approaching. They swerve directly at you. Time seems to crawl as panic hits. You desperately try to avoid the oncoming car, but a loud crash ensues. The violent jolt pushes you against your seatbelt, wind knocked out, vision blurred by flying windshield shards. The blare of horns, screeching tires, and your car's alarm create a disorienting noise. You attempt to move but are met with pain. The wrecked vehicle lies nearby. Thoughts whirl: \"Was it my fault?\" Shaking, you reach for your phone to call for help. Surrounding sounds amplify: sirens, murmurs from assisting drivers, your own labored breathing. Overwhelmed with fear, memories flood in, making you question if you'll ever drive confidently again."
    
    elif cue == 'ambush':

        if length=='long':
            instructions = "In the merciless grip of the midday sun, the desert becomes a vast, glaring oven. Each grain of sand below seems to pulse with latent menace. Your truck, sandwiched in the heart of a convoy, feels like a metal trap. Every pore on your face tightens, every nerve strung to breaking point. You're hyper-aware, the weight of potential danger causing the very air to thicken around you. Without warning, a deafening explosion ruptures the silence, its violent shockwave sending a visceral jolt down your spine. Your heart doesn't just race; it gallops, threatening to leap out of your chest. The once-organized procession is now a scene of pandemonium, dominated by a monstrous plume of smoke where the lead truck once was. An icy dread laces your veins with the horrifying realization: \"They've been obliterated.\" Everywhere you turn, you're met with a blinding, choking haze. A cacophony of shouts and orders, desperate and filled with panic, assaults your ears. But they sound distant, as if underwater, drowned out by the screaming alarm in your mind. Every fiber of your being feels electrified, vibrating with a frenzied energy. Commands echo around you, yet they seem abstract, distant. Your gut churns, twisting in on itself, each second stretching into an agonizing eternity. Amid the turmoil, a paralyzing thought hits: you've lost track of your position, your duty. Your mind races, thoughts scattering like leaves in a storm. Hands slick with sweat clutch your weapon so hard it's painful. Its cold metal feels volatile, ready to explode. The trigger yields beneath your grip, shots firing haphazardly. With every deafening report, the vision of home, of family, becomes more distant, more unreachable. The sharp, acrid stench of explosives fills your nostrils, a constant reminder of the looming threat. Waves of nausea, dread, and raw vulnerability crash over you, pulling you deeper into a vortex of overwhelming terror"

        elif length=='brief':
            instructions = "In the relentless desert sun, the horizon quivers with tension. You're part of a convoy, a vulnerable dot amidst endless dunes. As your skin prickles with the heat, an earth-shattering blast rips through the silence, so close that it's disorienting. Panic instantly floods your senses. \"The lead truck... obliterated,\" the realization hits like a sledgehammer. The surrounding atmosphere becomes a swirling mess of blinding smoke and chaos, while distant, desperate commands attempt to pierce through your mounting panic. Your every instinct is on overdrive; your stomach clenches with dread, your heart gallops uncontrollably. Amidst this bedlam, you've lost your focus, your duty a forgotten whisper. Sweaty palms grip your weapon, discharging rounds haphazardly. The pungent stench of explosives is suffocating. Thoughts of home, love, and safety seem cruelly distant as you're consumed by an all-encompassing terror."

    else:
        raise NotImplementedError

    return instructions

def retrieve_relaxation(cue, length):

    if cue=='generic':

        if length=='long':
            instructions = "Close your eyes and take a few deep breaths, inhaling through your nose and exhaling through your mouth. Imagine a path in front of you. This path leads to your safe space. You begin to walk down this path, noticing the sensations under your feet. Maybe it's soft grass, warm sand, or cool cobblestones. As you continue walking, you'll see the entrance to your safe space. It could be a cozy cabin, a serene beach, a lush forest, or any place that resonates with you. Step inside. Look around. What do you see? Are there vibrant colors or soothing shades? Listen carefully. Are there sounds that comfort you, like waves crashing or birds singing? Take a deep breath. What scents are in the air? Feel the environment. Is it warm, cool, or just right? This is your personal sanctuary. Here, you are safe, loved, and protected. Feel the peace that this space offers. If you like, you can invite positive affirmations into this moment, such as \"I am safe,\" or \"I am at peace.\" If you wish, find a comfortable spot within your safe space. Absorb its energy, knowing you can return here whenever you need. When you're ready, slowly retrace your steps back to the path that led you here. As you walk, carry the feelings of safety and tranquility with you. Gradually become aware of your surroundings. Wiggle your fingers and toes. When you feel ready, open your eyes. Take a moment to reflect on the experience. Remember, this safe space is always accessible to you, whenever you need a moment of peace and safety."
        
        elif length=='brief':
            instructions = "Close your eyes and take a deep breath. Imagine a path leading to your safe space. As you walk, feel the ground beneath, be it soft grass or warm sand. Soon, you're at the entrance to your sanctuary—maybe a cozy cabin or serene beach. Step inside and absorb the calming surroundings. Listen to the comforting sounds, like distant waves or birdsong. Breathe in familiar, soothing scents. This is where you are safe and at peace. Whisper to yourself, \"I am safe.\" Embrace this tranquility, knowing you can return anytime. When ready, slowly walk back, bringing this serenity with you. Gradually become present, wiggle your fingers and toes, and open your eyes. This sanctuary is always within reach."

    elif cue=="winter":
        
        if length=='long':
            instructions = "Close your eyes and take a few deep breaths, inhaling through your nose and exhaling through your mouth. Imagine a snowy trail ahead of you, stretching through the heart of a serene mountain range. You start walking on the snow-covered path, feeling the gentle crunch beneath your boots. The chill of the air is invigorating, but you are comfortably warm in your winter attire. As you journey along, the magnificent snowy peaks tower around you, and soon you come upon an opening that leads to your winter sanctuary. It might be a cozy mountain chalet, or a snow-covered meadow surrounded by ancient pines. Whatever it is, it resonates deeply with your heart. You step into your sanctuary and take a moment to look around. Maybe there's a warm, glowing fire, casting dancing shadows around. Icicles shimmer in the soft light, and the world outside is painted in shades of white and blue. The silence of the mountains is profound, only broken occasionally by the hush of the wind. Taking a deep breath, the crisp mountain air fills your lungs, mingling with the scent of pine and perhaps a hint of woodsmoke. Feel the ambiance of this place. It's calm, embracing, and just right for your soul. Whispering positive affirmations such as, \"I am embraced by the mountains,\" or \"I am at peace with nature,\" immerse yourself fully in this winter wonderland. You might choose a spot to sit, perhaps near the fire or looking out over the snow-laden trees. Bask in the serenity of your mountain sanctuary, drawing strength and tranquility from its beauty. When you're ready, begin your journey back down the snowy trail, bringing with you the calm and peace you've found. As you approach the path's beginning, start to become aware of your surroundings. Gently move your fingers and toes. When you feel grounded, open your eyes. "   

        elif length=='brief':
            instructions = "Take deep breaths, imagining a snowy mountain trail before you. Feel the crunch of snow beneath your boots as the invigorating chill of winter envelops you. The snow-clad peaks stand majestic, guiding you to a sanctuary - a cozy chalet or snow-kissed meadow. Stepping in, you're greeted by the warmth of a glowing fire. Icicles twinkle in its light, while the landscape outside is a canvas of white and blue. The profound mountain silence is punctuated only by the occasional whisper of wind. Breathe in the crisp air infused with pine and woodsmoke. Whisper affirmations like, \"I am embraced by the mountains,\" grounding yourself in this serene refuge. Choose a spot, either by the fire or overlooking snow-laden trees, and soak in the tranquility. Eventually, you make your way back, carrying the sanctuary's calm with you. As the trail's beginning nears, reconnect with reality, gently move your fingers and toes, and open your eyes, bringing mountain serenity into your day."

    elif cue=='sunset':

        if length=='long':
            instructions = "Close your eyes and breathe deeply, inhaling the scent of salty sea air. Imagine you're standing at the edge of a pristine tropical beach. The sand beneath your feet is warm and soft, each grain caressing your toes. As you look ahead, the sun is beginning its descent, casting the sky in hues of orange, pink, and purple. You take a gentle walk along the shoreline, the rhythmic sound of waves crashing softly against the sand accompanying you. Palm trees sway in the light breeze, their shadows growing long as the sun sinks lower. Before you is a comfortable spot, perhaps a hammock between two palms or a soft blanket on the sand, where you can rest and take in the sunset's full beauty. As you settle down, you feel the warmth of the last rays on your skin, mingling with the gentle sea breeze. The world seems to pause in this moment of serenity. Whisper to yourself affirmations like, \"I am one with nature,\" or \"I find peace in this moment.\" Let the soothing environment of the tropics wash over you, calming your mind and soul. When you're ready, gently stand, leaving the beach's embrace but carrying its tranquility with you. Begin to reconnect with your surroundings. Wiggle your fingers and toes, and when you feel present, slowly open your eyes, taking the tropical sunset's peace and beauty with you into your day."

        elif length=='brief':
            instructions = "Inhale deeply, taking in the scent of the ocean breeze. Picture yourself on a tropical beach, the soft, warm sand cushioning your feet. Ahead, the sun casts a breathtaking canvas of orange, pink, and purple, as it begins to set. Waves whisper against the shore as you walk, with palm trees rustling gently in the wind. Find a serene spot, maybe a hammock or blanket, perfect to absorb the sunset. As you settle, the sun's warmth and the sea breeze create a cocoon of serenity around you. The world seems to stand still in this tranquil moment. Silently affirm, \"I am at peace,\" allowing the beach's calm to envelope your being. As you rise, you carry this tranquility with you. Reconnect with reality, wiggle your fingers and toes, and open your eyes, the tropical sunset's serenity remaining with you."

    elif cue=="indian":
    
        if length=='long':
            instructions = "Close your eyes and breathe deeply, inhaling the sweet, earthy aroma of the fading summer. Envision yourself walking amidst the rich tapestry of an Indian summer, where the warmth of the season lingers even as the first signs of autumn emerge. The ground beneath you is a mosaic of crisp fallen leaves and resilient green grass, a testament to the season's transitional magic. Trees dressed in fiery reds, brilliant oranges, and deep yellows stand tall against a clear blue sky, their leaves occasionally dancing down, twirling in the gentle breeze. You continue your walk, feeling the sun's gentle warmth on your skin, tempered by a subtle coolness in the air. Fields stretch out, dotted with golden sunflowers turning towards the sun, their faces glowing with the vibrant energy of summer's end. Beside a tranquil pond, you take a moment to rest. The reflection in the water is a kaleidoscope of autumnal colors, shimmering with the sun's golden rays. The distant sound of migrating birds can be heard, as they journey to warmer lands, echoing the promise of the seasons changing. Whispering affirmations like, \"I embrace each moment,\" or \"I find beauty in transitions,\" you immerse yourself in the splendor of this fleeting time. As you prepare to leave this scene, slowly become aware of your surroundings. Move your fingers and toes, and when you're ready, open your eyes, carrying with you the warm and golden essence of an Indian summer."

        elif length=='brief':
            instructions = "Inhale deeply, embracing the earthy scent of a fading summer. Picture yourself amidst the Indian summer's enchantment, where warm hues blend with autumn's onset. The ground is a mix of crunchy leaves and green grass, showcasing nature's transitional beauty. Trees, adorned in vibrant reds, oranges, and yellows, contrast a pristine blue sky, their leaves playfully spiraling in the breeze. As you stroll, the sun kisses your skin, its warmth moderated by a hint of chill. Golden sunflowers stand tall in fields, their radiant faces basking in the sunlight. By a serene pond, you pause, its surface mirroring the dazzling autumn shades. Distant birds sing of their impending journeys, heralding the seasonal shift. Whispering affirmations, you cherish this ephemeral magic. Slowly reconnect with reality, wiggle your fingers and toes, and as you open your eyes, carry with you the essence of an Indian summer."

    elif cue=='body':

        instructions = "Imagine a path in front of you. This path leads to your safe space. What is the first place that comes to your mind? In this place, you are safe. Nobody can come here without your invitation. Look around. What do you see? Are there vibrant colors or soothing shades? Are there sounds that comfort you? What scents are in the air? How is the ground? Is it rock, or sand, or earthy soil? This is your personal sanctuary. Here, you are safe, loved, and protected. Feel the peace that this space offers. If you like, you can invite positive affirmations into this moment, such as \"I am safe,\" or \"I am at peace.\" If you wish, find a comfortable spot within your safe space. Absorb its energy, knowing you can return here whenever you need. When you're ready, slowly retrace your steps back to the path that led you here. As you walk, carry the feelings of safety and tranquility with you. Gradually become aware of your surroundings. When you feel ready, open your eyes. Take a moment to reflect on the experience. Remember, this safe space is always accessible to you, whenever you need a moment of peace and safety."

    elif cue=='chatgpt':

        instructions = "Close your eyes and take a moment to center yourself, breathing deeply and releasing any tension. Imagine yourself standing on the balcony of a high-rise apartment, overlooking a vast city during twilight. The sky above is painted in shades of lavender and deep blue, with the first stars of the evening starting to twinkle. Below, the city is a tapestry of twinkling lights, with cars moving like luminous beetles and skyscrapers outlined in gentle illuminations. Despite its vastness, there's an overwhelming sense of serenity. The usual cacophony of the city has softened into a distant hum, reminiscent of a lullaby sung by the universe. A gentle breeze caresses your face, carrying with it the faint, nostalgic scent of rain on warm asphalt. You lean forward, resting your arms on the balcony's edge, feeling the cool metal beneath your fingers. Looking down, you see pockets of life – a couple walking their dog, a street musician strumming a guitar, and children chasing fireflies. Their laughter and melodies drift upwards, mingling with the evening air. Allow yourself to be fully present in this moment, embracing affirmations like, \"I am at peace with the world,\" or \"I find beauty in stillness.\" Slowly, as you're ready to transition back, take another deep breath. Begin to notice your immediate environment. Gently wiggle your fingers and toes, grounding yourself. When you feel anchored, open your eyes, holding onto the serene essence of a city at twilight."

    else:

        raise NotImplementedError

    return instructions

def retrieve_stai(question_number):

    return ''