# weeInvaders
space invaders butt better

## todo
1. Menu

    So like the game should start in the menu screen,
    it should probs have like: New Game, Continue, Levels,
    Settings
    
    When the game ends due to death, should allow retry level
    or go back to Menu
    
    When game ends due to win, can continue to next level or 
    back to the Menu
    
    Would have to add mouse clicks for event check i guess

2. Enemy Movement

    So enemies should also be able to move only vertically.
    Possibly within the enemy definition dictionary can add 
    something like "movement_type", define a new vertical 
    movement system and check movement type when drawing enemies
     
3. Levels

    So, would have to create a few levels first.
    
    Then somehow add them into the game... I guessss there should
    just be a global counter of the level, which only gets updated 
    when u win OR reset when u start a new game
    
    Aha so also need some sort of saving function. Need to 
    check how to save to system in python/ pygame ?
    
    Also would be sick to create a screen where all levels are shown.
    So in each level definition would be cool to define an image for 
    the level thumbnail. 
    Would have to look into how to implement scrolling (if list of 
    levels big enough)