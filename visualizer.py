import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def load_off(file_path):
    vertices = []
    faces = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        if lines[0].strip() != 'OFF':
            print("Invalid OFF file format.")
            return vertices, faces

        num_vertices, num_faces, _ = map(int, lines[1].split())

        for line in lines[2:num_vertices + 2]:
            vertex = list(map(float, line.split()))
            vertices.append(vertex)

        for line in lines[num_vertices + 2:num_vertices + num_faces + 2]:
            # Ignoring the number of vertices in each face
            face = list(map(int, line.split()))[1:]
            faces.append(face)

    return vertices, faces


def draw_model(vertices, faces):
    glEnable(GL_DEPTH_TEST)

    # Render filled faces
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    for face in faces:
        glColor4f(0.5, 0.7, 1.0, 0.5)
        glBegin(GL_POLYGON)
        for vertex_index in face:
            glVertex3f(vertices[vertex_index][0],
                       vertices[vertex_index][1],
                       vertices[vertex_index][2])
        glEnd()

    glDisable(GL_BLEND)

    # Render wireframe (thinner or hidden behind faces)
    glEnable(GL_LINE_SMOOTH)
    glLineWidth(1.0)
    glColor3fv((0.3, 0.2, 0.3))
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    for face in faces:
        glBegin(GL_POLYGON)
        for vertex_index in face:
            glVertex3f(vertices[vertex_index][0],
                       vertices[vertex_index][1],
                       vertices[vertex_index][2])
        glEnd()
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glDisable(GL_DEPTH_TEST)


def main():
    filename = sys.argv[1]
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # model_path = "your_model.off"
    model_path = filename
    print(model_path)
    vertices, faces = load_off(model_path)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    rotation_speed = 1.0
    movement_speed = 1.0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # Rotate around X-axis (up)
                    glRotatef(rotation_speed, 1, 0, 0)
                elif event.key == pygame.K_DOWN:
                    # Rotate around X-axis (down)
                    glRotatef(-rotation_speed, 1, 0, 0)
                elif event.key == pygame.K_LEFT:
                    # Rotate around Y-axis (left)
                    glRotatef(rotation_speed, 0, 1, 0)
                elif event.key == pygame.K_RIGHT:
                    # Rotate around Y-axis (right)
                    glRotatef(-rotation_speed, 0, 1, 0)
                elif event.key == pygame.K_w:
                    # Move forward in Z-axis
                    glTranslatef(0, 0, movement_speed)
                elif event.key == pygame.K_s:
                    # Move backward in Z-axis
                    glTranslatef(0, 0, -movement_speed)
                elif event.key == pygame.K_a:
                    glTranslatef(-movement_speed, 0, 0)  # Move left in X-axis
                elif event.key == pygame.K_d:
                    glTranslatef(movement_speed, 0, 0)  # Move right in X-axis
                elif event.key == pygame.K_q:
                    # Move forward in Y-axis
                    glTranslatef(0, movement_speed, 0)
                elif event.key == pygame.K_e:
                    # Move backward in Y-axis
                    glTranslatef(0, -movement_speed, 0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_model(vertices, faces)
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
