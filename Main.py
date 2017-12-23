import arcade as ac
from random import *

# Written by /u/TDuffin, 22/12/2017.
# Example of a state machine adapted for the Arcade library, an alternative to PyGame.

class Game(ac.Window):
    """This class is the 'brain' of your game. It handles all of the events and updates for your game,
    and then sends them the appropriate scene/level/menu. It also handles changing (flipping) these states,
    and closing the game when you finish."""

    def __init__(self, width, height, states, initial_state):
        """The __init__ function is called whenever an instance of the Game class is created. This function
        initialises some variables that Arcade uses to create the game window, and sets the 'initial state'.
        The 'initial state' is the first scene which your game will load."""
        super().__init__(width, height)
        self.states = states
        self.state = self.states[initial_state]()
        self.persist = {}
        self.state.setup(self.persist)

    def on_draw(self):
        """Called once every frame when a new frame is drawn.
        arcade.start_render() must be called before your program starts drawing things to the screen."""
        ac.start_render()
        self.state.draw()

    def on_key_press(self, key, mod):
        """Whenever a key is pressed, send the event info to the state"""
        self.state.key_down(key, mod)

    def on_key_release(self, key, mod):
        """Whenever a key is released, send the event info to the state"""
        self.state.key_release(key, mod)

    def update(self, delta_time):
        """Called once every frame, allowing the user to program game logic into their scenes. Check_state is called
        to check if the program needs to flip to the next state.
        delta_time is the time since the last frame in ms"""
        self.check_state()
        self.state.update(delta_time)

    def check_state(self):
        """If the 'done' variable is set to true inside of the state, the program calls the flip_state function.
        If the 'quit' variable is set to true, the program quits"""
        if self.state.done:
            self.flip_state()
        if self.state.quit:
            quit()

    def flip_state(self):
        """This function changes the program to the next scene, then runs its startup method."""
        persist = self.state.persist
        self.state.done = False
        self.state = self.states[self.state.next_state]()
        self.state.setup(persist)


class State(object):
    """This is the parent class of all scene/state classes in your game."""

    def __init__(self):
        """Initialises the state's variables
        'persist' is a dictionary which can store information to be accessed between states.
        'done' tells the program to flip the states
        'next_state' stores a dictionary key from the state dictionary, the program will flip to this state later"""
        self.persist = {}
        self.next_state = None
        self.done = False
        self.quit = False

    def setup(self, persist):
        """Startup is used to set certain variables to a 'default' state in your program, and is called every time
        the state is started again by the program."""
        self.persist = persist

    def key_down(self, key, mod):
        """Called by the Game class when a user presses a key down"""
        pass

    def key_release(self, key, mod):
        """Called by the Game class when a user releases a key"""
        pass

    def update(self, dt):
        """Updates the scene every frame"""
        pass

    def draw(self):
        """Draws the scene's elements every frame"""
        pass


class MainMenu(State):
    """Example the initial state of your game. Every frame this draws a background with different shades of Red,
    with text drawn on top."""
    def __init__(self):
        super(MainMenu, self).__init__()

    def setup(self, persist):
        """Example of using the persist dictionary to pull data from between scenes."""
        self.persist = persist
        self.text = "Scene One.\nPress Space to Change Scenes,\nPress Esc. to Exit."
        self.text_position = self.persist.get("text_position", [0, 300])

    def key_down(self, key, mod):
        """Example of switching between states,
         and using the persistent dictionary to set the new position of the text"""
        if key == ac.key.ESCAPE:
            self.quit = True
        if key == ac.key.SPACE:
            self.text_position[0] += 10
            self.text_position[1] += 10
            self.persist["text_position"] = self.text_position
            self.done = True
            self.next_state = "SCENE"

    def update(self, dt):
        """Example of logic processing in a scene.
        Called once per frame by the Game class. This example sets the colour of the background to a shade of Red"""
        x = randint(150, 200)
        self.col = (255, x, x)

    def draw(self):
        """Draws the elements to the screen."""
        ac.set_background_color(self.col)
        ac.draw_text(self.text, self.text_position[0], self.text_position[1], ac.color.BLACK, 14, anchor_y="top")


class Scene(State):
    """Example of a second scene in your game. This one is similar to the previous apart from that the colour is a
    shade of Green instead of red."""

    def __init__(self):
        super(Scene, self).__init__()

    def setup(self, persist):
        self.persist = persist
        self.text = "Scene Two.\nPress Space to Change Scenes,\nPress Esc. to Exit."
        self.text_position = self.persist.get("text_position", [0, 300])

    def key_down(self, key, mod):
        if key == ac.key.ESCAPE:
            self.quit = True
        if key == ac.key.SPACE:
            self.text_position[0] += 10
            self.text_position[1] += 10
            self.persist["text_position"] = self.text_position
            self.done = True
            self.next_state = "MAIN"

    def update(self, dt):
        x = randint(150, 200)
        self.col = (x, 255, x)

    def draw(self):
        ac.set_background_color(self.col)
        ac.draw_text(self.text, self.text_position[0], self.text_position[1], ac.color.BLACK, 14, anchor_y="top")


def main():
    """Starts the game by initialising the 'Game' class, and calling 'arcade.run' """
    WIDTH = 600
    HEIGHT = 600

    # This dictionary stores the different states in your program, passed to the Game class at runtime.
    game_states = {
        "MAIN": MainMenu,
        "SCENE": Scene,

    }

    game = Game(WIDTH, HEIGHT, game_states, "MAIN")
    ac.run()

if __name__ == "__main__":
    """__name__ is equal to __main__ when this program is run by the user by running 'main.py'. This is only ever not
    true if the user were to import the file as a module. You don't really need to worry about this."""
    main()