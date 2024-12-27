## Catch Zone

Last Update: 12/27/2024

**Main Question**
Where do I have to sit in Yankee stadium in order to catch a home run baseball?

#### Method

**1. Data Collection**
First we select our hitting team and our pitching team. For this example, since it is the off season, we are going with the 2024 Yankees as our hitting team, and the 2024 Dodgers as our pitching team.

Second, we webscrape the team rosters from their respectivve team websites. Then, from ESPN, we webscrape their position as well as their relative priority in their respective position, e.g. Starters and Reliefs.

Then we use the pybaseball library to get the relevant hit level and pitch level data for each of them. We conducted a round of exploration and analysis, and did not find much significance in clustering based on characteristics like player or pitch type. Thus we can move on to our feature engineering and model building.

**2. Feature Engineering**
This ended up being less relevant than initially thought, so future iterations on this project may look to this as a key starting point. First we ran all the pitches and hits through our simulation (will go over this later) to remove enviromental and other confounding variable effects. We classified these as home runs or not based on the Yankee stadium layout.

We found the releative probability of a player appearing to pitch as well as the releative probability of each pitch type appearing as well as their relevant statistics. We found player weights and pitch weights based on appearence and role. We were able to combine all this to find the team level pitch distribution for a given team. Let us now build our model.

**3. Machine Learning**
We used an XGBoost model with a lot of input parameters in order to predict these values:

```
target_features = [
        'release_spin_rate',
        'launch_speed',
        'launch_angle',
        'spray_angle',
        'spin_axis',
        'plate_x',
        'plate_z'
    ]
```

We trained the model on our hitting team's performance. We then used our model to predict these above variables when our hitting team encountered our given pitching team. Thus, we have predicted these values and are able to now simulate where they might land.

**4. Running the Simulation**
We built our simulation based off of Alan Nathan's work for predicting baseball trajectories. The paper we based our implementation on can be found [here](https://baseball.physics.illinois.edu/TrajectoryAnalysis.pdf).

We run the output of our model through this simulation and find our final ball hitting locations.

We plot these and thus able to predict where we should sit in order to be most likely to catch a ball.

**5. Further Work**
I would like to make this more user friendly. Able to input any teams, any upcoming game date, and build a model off of that. In addition, some memoization such that we don't need to keep calling for and storing this data.
In addition, I would like the output to be much cleaner and user friendly. The main workhorse part is done, but for example, a heatmap of probabilities might be useful to a user. In addition, fine tuning the model a bit more or gathering larger datasets, or using more time series analysis. Further work can be done, but for now, it is a useful and good tool. Thank you for reading.
