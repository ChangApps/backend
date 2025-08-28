# backend

Requerimientos técnicos para la instalación
A continuación se detallan los requisitos técnicos y los pasos necesarios para instalar y ejecutar el sistema desarrollados ,solo backend.
    Requerimientos previos
       ○ Sistema operativo: Windows o Linux.
       ○ Git instalado para clonar los repositorios: https://git-scm.com/downloads
       ○ Python: Versión 3.8 o superior (descarga en https://www.python.org/downloads/).
       ○ Entorno virtual: Obligatorio en Linux/macOS, opcional en Windows.
    
1.Clonar el repositorio del backend:
       git clone https://github.com/ChangApps/backend
       Una vez clonado, abrir una terminal en la carpeta del proyecto y ejecutar:
                                                                                  cd backend

2.Activar entorno virtual (recomendacion) 
    En Linux/macOS:
    Se recomienda utilizar un entorno virtual para aislar las dependencias del proyecto.
                        python3 -m venv venv
                        source venv/bin/activate
    
    En Windows:
                El entorno virtual es opcional, pero puede activarse así:
                                 python -m venv venv       
                                 venv\Scripts\activate

3.Instalacion de dependencias 
     en la terminal ejecutar:
                            pip install django
                            pip install django-admin-interface
                            pip install djangorestframework
                            pip install django-cors-headers
                            pip install djangorestframework-simplejwt
                            pip install drf-yasg

4.Ejecutar el servidor
     en la terminal ejecutar (dependiendo de la version de python):
                                                                    python3 manage.py runserver
                                                                    python manage.py runserver
      Si todo sale correcto sale algo como esto:
                                            Django version 5.2.5, using settings 'proyecto.settings'
                                            Starting development server at http://127.0.0.1:8000/
                                            Quit the server with CONTROL-C.
      El servidor ya esta ejecutandose,para detenerlo CRTL+C.
