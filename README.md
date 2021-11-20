# Dodging-game

## Info

- Done by Niclas Heide
- Smaller fixes done by Jan Ruhfus(@JanKrb)

## Work order:

Set up an online GitHub repository (ITA-GIT if applicable). ALL project components should be stored there. Upload the link to the Git repository in Teams. Program a small application with the following requirements: 

1. Standard functionality: : 
   - Window has a decent size. 
   - Background is a matching bitmap or solid color. 
   - The application is terminated with the ESC key or by clicking on "X" with the mouse. 
   - All bitmaps are created as pygame.sprite.Sprite object and converted and scaled to fit after loading. 
   - All bitmaps - except the background - are transparent. 
   - All bitmaps - except for "lone fighter" or background - are stored in pygame.sprite.Group objects
   - The game has a running speed of 60fps. 
2.  Obstacles of various sizes are randomly generated at the top of the screen.  
3.  These move downwards at different speeds.  
4. If they arrive at the bottom, they are deleted.
5.  Bonus: If an obstacle arrives at the bottom, the score is increased by 1. 
6.  Bonus: The score is displayed in the upper left corner. 
7.  At the bottom is a player bitmap, which can be controlled by arrow keys in all four directions. 
8.   If the player collides with an obstacle, he starts again at the bottom center; make sure that there is no obstacle there. 
9.  The player has three lives. 
10. Over time, the obstacles become faster (up to a reasonable upper limit).  
11. In the course of time, more and more frequent (reasonable upper limit!) obstacles are created.
12. Bonus: After releasing the SPACE key, the player bitmap should jump to a new randomly selected position. The new position must be chosen so that the bitmap is always fully visible and does not collide with an obstacle. This possibility shall be available only three times for the whole game.

### Evaluation basis 

- Completeness and correctness with regard to the task definition
- Choosing the right Python and PyGame functionalities 
- Sourcecode formatting and commenting 
- Aesthetics 

## Controls:

- Key up = Move up
- Key down = Move down
- Key left = Move left
- Key right = Move right
- Key "P" = Pause Screen
- Key "ESC" = Leave game

