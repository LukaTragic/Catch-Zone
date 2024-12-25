# Catch-Zone

#### Basic Question

I want to catch a baseball at a baseball game. Where should I sit?

11/16

- Added webscraping roster functionality
- Isolated teams by home game and home runs

11/28

- Beginning to reference Alan Nathan's implementation
- Talked to David to figure out calculations
- found velocity and spin values in each direction

12/1

- finished successfully calculating velocity and accleration of each direction

12/3

- able to iterate and find trajectory of a given row in the database
- able to simulate it for each time step

12/12

- fixed trajectory
- refactored and reorganized a bunch of code

12/13

- reorganized some things
- begining to outline machine learning model
- tested correlation of the variables I am trying to predict, looks promising

12/14

- using correlation matrix to test if input variables of our simulation are correlated or not. They are not correlated with each other.
- used one way Anova test to determine if player stats are statistically significant enough to each other, they seem to be, suggestive of clustering

12/19

- FIGURED OUT HOW I AM GOING TO DO THINGS
  Project Workflow:
  GIVEN AN UPCOMING GAME, WHERE DO I SIT?#

**Data Collection and Preprocessing**

- Collect data on batters, pitchers, and hit level data and store and organize into databases
- Calculate temporal weights for each appearance/event

**Feature Engineering**

- Create rolling averages for key metrics
- Build temporally weighted player statistics

**Model Development**

- Goal here is to predict how the opposing team will pitch, then using the pitch data, we will predict how a batter will hit the ball
- Perhaps we can cluster out the types of pitches this team does and weight how likely they are to occur. Then we predict how the Yankees will react to pitches like those. Then we are able to use that to predict values.
- Split the data temporally
- Train and Cross Validate model on predictions
- Tune hyperparamters

**Simulate**

- Once we are able to predict how a batter will hit the ball, we will run all such values through our simulation.
- We will scrape the weather prediction of the date and also input that into our simulation.
- We will end up with a list of coordinates and their associated probability (based on how likely it is to be pitched/responded to) and create a heat map to show where the ball will land

12/25

- Merry Christmas
- Adjusted A LOT OF THINGS ABOUT THE METHOD AND EVERYTHING
- found team pitch distribution
- added player weights

TO DO:

- pick and run model
- classify home runs and integrate into main data frame
- hitter weight classification

- ALL OF THE ABOVE
