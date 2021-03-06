
from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math



# Create your objects here.
hub = MSHub()

#variable des moteurs
Mpair = MotorPair('F','E')
robot = MotorPair('F','E')
invertMpair = MotorPair('E','F')
motorL = Motor('E')
motorR = Motor('F')
topModule = Motor('D')
frontMotor = Motor('C')
backMotor = Motor('D')
#tourner à 90 degrés
#reset le yaw du gyro
hub.motion_sensor.reset_yaw_angle()
#variable de l'angle de destination
"""
val = 90
pair.start_tank(8, -8)
while hub.motion_sensor.get_yaw_angle() <= val:
    print(str(hub.motion_sensor.get_yaw_angle()))
    pass
pair.stop()
print(str(hub.motion_sensor.get_yaw_angle()))
"""

# la fonction pour tourner avec le gyro
# elle prend en paramètre la paire de moteurs et l'angle demandé
# il y environ 2 degrés de marge
def gyroTurn(motors, angle,speed = 8):
    hub.motion_sensor.reset_yaw_angle()
    #vérifie si la valeur est positiver est négative
    #divise angle par la valeur absolue de l'angle (si angle = -1 alors valeur absolue = 1 et à l'inverse si angle = 1 alors valeur absolue = -1)
    #si l'angle est négatif, l'angle = 1 et si ml'angle est positif, angle = -1
    direction = angle / math.fabs(angle)
    print("direction:",direction)
    motors.start_tank(speed*int(direction),-speed*int(direction))
    print("direction:",direction)
    # example: -1*2 <= -1*-90
    # donc, si -2 <= 90
    while direction*hub.motion_sensor.get_yaw_angle() <= direction*angle:
        print(str(hub.motion_sensor.get_yaw_angle()))
        pass
    motors.stop()
    print(str(hub.motion_sensor.get_yaw_angle()))

def progressiveGyroturn(robot, angle):
    def get_distance(a, b):
        return int(math.fabs(math.fabs(a) - math.fabs(b)))
    robot.set_stop_action('brake')
    hub.motion_sensor.reset_yaw_angle()
    direction = int(angle / math.fabs(angle)) # 1 is clockwise,-1 is counterclockwise
    current_angle = 0
    distance = angle * direction
    speed = 0
    while current_angle*direction < angle*direction:
        print("current:",current_angle)
        robot.start_tank(speed* direction, speed*direction*-1)
        current_angle = hub.motion_sensor.get_yaw_angle()
        distance = get_distance(current_angle, angle)
        speed = int(distance / math.fabs(angle) * 20) + 5 # we get a number between 5 and 30
    robot.stop()
#carré
def square(speed,gyroSpeed = 10):
    pair.set_stop_action('coast')
    for i in range(4):
        moveForwardCm(Mpair,10,30)
        gyroTurn(pair,-90,gyroSpeed)

# fonction qui retourne un tour de roue
# cette fonction prnd en paramètre le type de roue("little" pour petit et "big" pour gros)
def setWheelType(whell = "small"):
    # vérifie si le paramètre est égal à "small"
    if whell == "small":
        #le diamètre des roues
        rotation = 5.6 * math.pi
        pair.set_motor_rotation(rotation, 'cm')
    else:
        # ici, dans tous les cas, le paramètre estv égal à small
        rotation = 8.8 * math.pi
        pair.set_motor_rotation(rotation, 'cm')

#fonction pour afficher simplement du texte sur le HUB
def hubPrint(hubVar,text = "LES BRAINSTORMEURS C'EST LES MEILLEURS !!!"):
    hubVar.light_matrix.write(str(text))

def moveForward(pair,degrees,speed = 100):
    #calcul du coefficient de proportionnalité
    # on finit à accélérer à 2 cm
    # intialise la rotation du moteur
    motorL.set_degrees_counted(0)
    LIMIT = degrees/2
    while(True):
        currentSpeed = 0
        current = math.fabs(motorL.get_degrees_counted())
        if current <= LIMIT:
            #on est entre les deux
            currentSpeed =current*90/LIMIT+10
        elif current >= degrees-LIMIT:
            currentSpeed =100-((current-(degrees-LIMIT))*90/LIMIT+10)
        else:
            currentSpeed = 100
        if current >= degrees:
            break
        pair.start_tank(int(currentSpeed),int(currentSpeed))
        print("current",current,"speed", currentSpeed)

    pair.stop()

def moveForwardCm(pair,distanceCm,speed = 100):
    #calcul du coefficient de proportionnalité
    # on finit à accélérer à 2 cm
    # intialise la rotation du moteur
    Wheelperimeter = 5.6*math.pi
    print("wheel perimeter = ",Wheelperimeter)
    coefCmDegrees = 360/Wheelperimeter
    print("coefCmDegrees",coefCmDegrees)
    degrees = distanceCm*coefCmDegrees
    print("degrees",degrees)
    motorL.set_degrees_counted(0)
    LIMIT = degrees/2
    while(True):
        currentSpeed = 0
        current = math.fabs(motorL.get_degrees_counted())
        if current <= LIMIT:
            #on est entre les deux
            currentSpeed =current*(speed-10)/LIMIT+10
        elif current >= degrees-LIMIT:
            currentSpeed =speed-((current-(degrees-LIMIT))*(speed-10)/LIMIT+10)
        else:
            currentSpeed = speed
        if current >= degrees-4:
            break
        pair.start_tank(int(currentSpeed),int(currentSpeed))
        print("current",current,"speed", currentSpeed)
    pair.stop()

# la fonction du gyro turn pour un mot
def gyroTurnOneMotor(motors, angle,speed = 8):
    hub.motion_sensor.reset_yaw_angle()
    #vérifie si la valeur est positiver est négative
    #divise angle par la valeur absolue de l'angle (si angle = -1 alors valeur absolue = 1 et à l'inverse si angle = 1 alors valeur absolue = -1)
    #si l'angle est négatif, l'angle = 1 et si ml'angle est positif, angle = -1
    direction = angle / math.fabs(angle)
    print("direction:",direction)
    motors.start_tank(0,-speed*int(direction))
    print("direction:",direction)
    # example: -1*2 <= -1*-90
    # donc, si -2 <= 90
    while direction*hub.motion_sensor.get_yaw_angle() <= direction*angle:
        print(str(hub.motion_sensor.get_yaw_angle()))
        pass
    motors.stop()
    print(str(hub.motion_sensor.get_yaw_angle()))

def autoCleaning():
    Mpair.start()

def delay(seconds):
    hub.wait_for_seconds(seconds)

def platooningTrucks():
    #moveForwardCm(Mpair,40)
    Mpair.move(41,'cm',0,30)
    hub.motion_sensor.reset_yaw_angle()
    progressiveGyroturn(Mpair,90)
    #motorL.run_for_degrees(-265,30)
    Mpair.move(45,'cm',0,30)
    motorL.run_for_degrees(80,30)
    canon()
    oscillate(2)
    motorL.run_for_degrees(-40,30)

    motorL.run_for_degrees(-80,30)
    Mpair.move(100,'cm',0,-100)

"""
    #avancer de 66 cm
    Mpair.move(70,'cm',0,60)
"""
def turbinBlade():
    Mpair.move(60,'cm',0,100)
    Mpair.move(60,'cm',0,-100)
"""
moveForwardCm(Mpair,10,30)
gyroTurn(Mpair,90,10)
"""

def oscillate(number):
    for i in range(number):
        motorL.run_for_degrees(-40,30)
        motorL.run_for_degrees(80,30)
        motorL.run_for_degrees(-80,30)

def canon():
    print("BOUUUM !")
    Motor('D').run_for_degrees(-200,30)
def initAirplaneModule():
    frontMotor.run_to_position(359, 'clockwise', 75)
def switchEngine():
    invertMpair.set_default_speed(30)
    invertMpair.move(-10, 'cm', 0, 20)
    motorL.run_for_degrees(int(45/(1/3)), -30)
    invertMpair.move(-20, 'cm', 0, 20)
    motorL.run_for_degrees(int(45/(1/3)), 30)
    invertMpair.move(-70, 'cm', 0, 50)
    frontMotor.run_for_degrees(-100, 30)
    #je recule avant le moteur
    invertMpair.move(10, 'cm', 0, 30)
    # je monte le moteur
    frontMotor.run_for_degrees(100, 20)
    invertMpair.move(7, 'cm', 0, 20)
    invertMpair.move_tank(-135/(180/273), 'degrees', 10, -10)
    invertMpair.move(2, 'cm', 0, 20)
    frontMotor.run_for_degrees(-100, 100)
    #on retourne a la maison
    invertMpair.move_tank(-20/(180/273), 'degrees', 10, -10)
    invertMpair.move(-90, 'cm', 0, 100)

    """
    invertMpair.move(25, 'cm', 0, 30)
    motorL.run_for_degrees(int(45/(1/3)), 30)
    invertMpair.move(16, 'cm', 0, 20)
    frontMotor.run_for_degrees(-100, 20)
    frontMotor.stop()
    """
    """
    #on avance l'avion
    invertMpair.move(-25, 'cm', 0, 50)
    frontMotor.run_for_degrees(100, 20)
    frontMotor.stop()
    motorL.run_for_degrees(int(90/(1/3)), 30)
    invertMpair.move(11, 'cm', 0, 20)
    frontMotor.run_for_degrees(-100, 100)
    frontMotor.run_for_degrees(100, 20)
    invertMpair.move(-90, 'cm', 0, 100)
"""

def stopFrontMotor():
    frontMotor.stop()
"""
    invertMpair.set_default_speed(30)
    invertMpair.move(-73, 'cm', 0, 20)
    motorL.run_for_degrees(int(45/(1/3)), -30)
    invertMpair.move(-30, 'cm', 0, 20)
    motorL.run_for_degrees(int(45/(1/3)), 30)
    invertMpair.move(-1, 'cm', 0, 20)
    frontMotor.run_to_position(359, 'clockwise', 75)
    frontMotor.run_for_degrees(-150, 30)
    invertMpair.move(9, 'cm', 0, 20)
    frontMotor.run_to_position(359, 'clockwise', 40)
    invertMpair.move(-9, 'cm', 0, 20)
    motorL.run_for_degrees(int(45/(1/3)), -30)
    invertMpair.move(25, 'cm', 0, 20)
    motorR.run_for_degrees(int(90/(1/3)), 30)
    invertMpair.move(28, 'cm', 0, 20)
    frontMotor.run_for_degrees(-95, 30)
    invertMpair.move(33, 'cm', 0, -20)
    frontMotor.run_for_degrees(10, 30)
    motorR.run_for_degrees(int(90/(1/3)), 30)
    frontMotor.run_to_position(359, 'clockwise', 40)
    invertMpair.move(12, 'cm', 0, 20)
"""
"""
    topModule.set_degrees_counted(0)

    #topModule.run_to_degrees_counted(0, 50)
    #topModule.run_to_degrees_counted(176, 50)
    #topModule.run_to_position(0, 'shortest path', 75)

    invertMpair.set_default_speed(30)
    invertMpair.move(-71, 'cm', 0, 20)
    #moveForwardCm(Mpair,-70)
    # 35 : nombre de degrés que le robot doit parcourir
    # 1/3 coef de proportionnalité: 90 degrés du moteur donnent environ 0,3 degrés du robot
    motorL.run_for_degrees(int(-45/(1/3)), 30)
    #progressiveGyroturn(Mpair, 35)
    invertMpair.move(-35, 'cm', 0, 25)
    topModule.run_for_degrees(-180)
    #platooningTrucks()
    invertMpair.move(31, 'cm', 0, 25)
    motorL.run_for_degrees(int(90/(1/3)), 30)
    invertMpair.move(-4, 'cm', 0, 25)
    #airplane()
    airplaneModule2()
"""
#platooningTrucks()
#switchEngine()
def airplane():
    topModule.run_to_position(20, 'shortest path', 75)
    #topModule.run_for_seconds(1, -100)
    for i in range(3):
        topModule.run_for_degrees(250, 100)
        topModule.run_for_degrees(-250, 100)

#switchEngine()
#frontMotor.run_for_degrees(-100, 30)
#platooningTrucks()
#airplane()
#frontMotor.run_for_degrees(90,100)
def airplaneModule2():
    frontMotor.run_for_seconds(1, -100)
def missionPlatooningTrucks():
    invertMpair.move(-29, 'cm', 0, 30)
    motorR.run_for_degrees(int(-89/(1/3)), 20)
    invertMpair.move(-49, 'cm', 0, 30)
    invertMpair.move(80, 'cm', 0, 100)
    motorR.run_for_degrees(int(89/(1/3)), 100)

# la fonction du projet innovant
def innovationProject():
    pass
    
# la fonction du pont 
def bridge():
    invertMpair.move(22, 'cm', 0, 30)
    motorR.run_for_degrees(int(-89/(1/3)), 20)
    invertMpair.move(106, 'cm', 0, 30)
    motorR.run_for_degrees(int(44/(1/3)), 20)
    backMotor.run_for_degrees(35,10)
    frontMotor.run_for_degrees(75,10)
    invertMpair.move(-10, 'cm', 0, 30)
    motorR.run_for_degrees(int(135/(1/3)), 20)
    invertMpair.move(150, 'cm', 0, 100)
"""
Pendant la séance du 29/01/2022 nous avons créé un nouveau module et adapté le programme pour lui.
Nous avons fait la lmission de l'avion(qu'il fallait pousser)
or, le module ne montait pas assez haut, christophe l'a donc modifié
pour la prochaine séance, il faudra donc adapter le programme pour cette modification
"""

"""
Séance du 05/02/22
La mission de l'avion fonctionne presque en fin de run. Il ne manque plus qu'un callage
sur la ligne.
On pense utiliser le module du dessus pour positionner la brique tombée de l'avion
complètement dans le cercle
Avec le callage on a un run complet et on peut penser au suivant
"""
"""
séance du 12/02/22
On a décidé de faire l'avion avec la ligne plus tard.
La mission pour décharger l'avion cargo marche
On a le premier run complet
"""
"""
séance du 19/02/22
nous avons fait la mission du projet innovant mais elle ne marche pas vraiment et elle est à RETRAVAILLER
 
"""
switchEngine()
#bridge()
