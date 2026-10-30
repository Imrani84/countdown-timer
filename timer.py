from ursina import *
import math
app = Ursina(development_mode=False, size=(520, 390))


window.title = "Timer"



Values = {"hours":0, "minutes":0, "seconds":0}

hours_box = Text(text = f"{Values["hours"]:02}", origin = (0,0), position = (-0.1,0), scale = 3)
hours_text = Text(text = "hours", color = color.gray, origin = (0,0), position = (-0.1,-0.05))

first_colon = Text(text = ":", scale = 3, origin = (0,0), position = (-0.05,0.005))

minutes_box = Text(text = f"{Values["minutes"]:02}", origin = (0,0), scale = 3)
minutes_text = Text(text = "minutes", color = color.gray, origin = (0,0), position = (0,-0.05))

second_colon = Text(text = ":", scale = 3, origin = (0,0), position = (0.05,0.005))

seconds_box = Text(text = f"{Values["seconds"]:02}", origin = (0,0), position = (0.1,0), scale = 3)
seconds_text = Text(text = "seconds", color = color.gray, origin = (0,0), position = (0.1,-0.05))

def increase(variable, box):
    if Values[variable] < 59:
        Values[variable] += 1
        box.text = f"{Values[variable]:02}"
    elif Values[variable] == 59:
        Values[variable] = 0
        box.text = f"{Values[variable]:02}"

def decrease(variable, box):
    if Values[variable] > 0:
        Values[variable] -= 1
        box.text = f"{Values[variable]:02}"
    elif Values[variable] == 0:
        Values[variable] = 59
        box.text = f"{Values[variable]:02}"

h_up_arrow = Button(text = "^", text_size = 2, text_color = color.black, color = color.white, position = (-0.1,0.1), scale = 0.05, on_click = Func(increase, "hours", hours_box))
h_down_arrow = Button(text = "v",text_size = 2, text_color = color.black, color = color.white, position = (-0.1,-0.1), scale = 0.05, on_click = Func(decrease, "hours", hours_box))

m_up_arrow = Button(text = "^", text_size = 2, text_color = color.black, color = color.white, position = (0,0.1), scale = 0.05, on_click = Func(increase, "minutes", minutes_box))
m_down_arrow = Button(text = "v",text_size = 2, text_color = color.black, color = color.white, position = (0,-0.1), scale = 0.05, on_click = Func(decrease, "minutes", minutes_box))

s_up_arrow = Button(text = "^", text_size = 2, text_color = color.black, color = color.white, position = (0.1,0.1), scale = 0.05, on_click = Func(increase, "seconds", seconds_box))
s_down_arrow = Button(text = "v",text_size = 2, text_color = color.black, color = color.white, position = (0.1,-0.1), scale = 0.05, on_click = Func(decrease, "seconds", seconds_box))


Texts = [hours_box, hours_text, first_colon, minutes_box, minutes_text, second_colon, seconds_box, seconds_text]

Buttons = [
    (h_up_arrow, increase, "hours", hours_box),
    (h_down_arrow, decrease, "hours", hours_box),
    (m_up_arrow, increase, "minutes", minutes_box),
    (m_down_arrow, decrease, "minutes", minutes_box),
    (s_up_arrow, increase, "seconds", seconds_box),
    (s_down_arrow, decrease, "seconds", seconds_box)
]

hold_timer = 0

def update():
    global hold_timer, running, remaining
    Holding = False
    for button, action, variable, box in Buttons:
        if button.hovered == True and held_keys["left mouse"]:
            hold_timer += time.dt
            Holding = True
            if hold_timer >= 0.05:
                action(variable, box)
                hold_timer = 0
    if Holding == False:
        hold_timer = -0.45

    if running == True:
        remaining -= time.dt
        secs = math.ceil(remaining)
        hours = secs // 3600
        minutes = secs // 60 % 60
        seconds = secs % 60
        timer_box.text = f"{hours:02}:{minutes:02}:{seconds:02}"
        if secs <= 0:
            running = False
            timer_box.enabled = False
            timesup.enabled = True
            stop_button.enabled = False
            pause_button.enabled = False
            ok_button.enabled = True











def pause_timer():
    global running
    running = False
    pause_button.enabled = False
    resume_button.enabled = True

def resume_timer():
    global running
    running = True
    resume_button.enabled = False
    pause_button.enabled = True

def stop_timer():
    global running
    running= False
    timer_box.enabled = False
    stop_button.enabled = False
    pause_button.enabled = False
    start_button.enabled = True
    timesup.enabled = False
    ok_button.enabled = False
    resume_button.enabled = False
    for button, action, variable, box in Buttons:
        button.enabled = True
    for texts in Texts:
        texts.enabled = True

timesup = Text(text = "TIMES UP", scale = 5, color = color.red, origin = (0,0), enabled = False)
stop_button = Button(text = "STOP TIMER", text_color = color.white, color = color.red, origin = (0,0), position = (-0.15,-0.2), scale = (0.2,0.1), enabled = False, on_click = stop_timer)
pause_button = Button(text = "PAUSE TIMER", text_color = color.white, color = color.orange, origin = (0,0), position = (0.15,-0.2), scale = (0.2,0.1), enabled = False, on_click = pause_timer)
resume_button = Button(text = "RESUME TIMER", text_color = color.black, color = color.green, origin = (0,0), position = (0.15,-0.2), scale = (0.2,0.1), enabled = False, on_click = resume_timer)
ok_button = Button(text = "OK", color = color.green, text_color = color.black, origin = (0,0), position = (0,-0.2), scale = (0.15,0.1), enabled = False, on_click = stop_timer)

timer = f"{Values["hours"]:02}:{Values["minutes"]:02}:{Values["seconds"]:02}"
timer_box = Text(text = timer, scale = 4, origin = (0,0), color = color.white, enabled = False)

running = False
remaining = 0

def start_timer():
    global timer, running, remaining
    remaining = Values["hours"]*3600 + Values["minutes"]*60 + Values["seconds"]
    running = True

    timer = f"{Values["hours"]:02}:{Values["minutes"]:02}:{Values["seconds"]:02}"
    timer_box.text = timer
    timer_box.enabled = True
    start_button.enabled = False
    stop_button.enabled = True
    pause_button.enabled = True
    for button, action, variable, box in Buttons:
        button.enabled = False
    for texts in Texts:
        texts.enabled = False

start_button = Button(text = "START TIMER", text_color = color.black, color = color.green, origin = (0,0), position = (0,-0.2), scale = (0.2,0.1), on_click = start_timer)















#this part is to fix the size of the window and ui and was made by claude ai
S = 2.2

everything = Texts + [b[0] for b in Buttons] + [
    timer_box, timesup,
    start_button, stop_button, pause_button, resume_button, ok_button
]

for e in everything:
    e.position = (e.x * S, (e.y + 0.0625) * S) 
    e.scale = e.scale * S

for b in [row[0] for row in Buttons] + [start_button, stop_button, pause_button, resume_button, ok_button]:
    b.text_size = b.text_size * S
all_buttons = [row[0] for row in Buttons] + [start_button, stop_button, pause_button, resume_button, ok_button]

for b in all_buttons:
    b.highlight_text_size = b.text_size * 1.1

app.run()

