# FC-I-UP_2026-2
Repositorio de código y tareas escritas del curso de Física Computacional I para físicos 2026-2

## Asignaciones
### Semana 1
**Actividades**
# Plan de Clase: Version Control in Science

**Asignatura:** Física Computacional 1

**Unidad:** Unidad 1 — Introducción a Python (Sección: Introducción a Git, GitHub y Colaboratory)

**Lectura asociada:** Ram, K. (2013). *[Git can facilitate greater reproducibility and increased transparency in science -
Karthik Ram]*(https://pmc.ncbi.nlm.nih.gov/articles/PMC3639880/). Source Code for Biology and Medicine.

---

### Fase 1: Trabajo Independiente (Preparación y Práctica Técnica)

Los estudiantes realizan la lectura individual del artículo en casa, cumpliendo con el mecanismo de control de lectura en lengua inglesa establecido en la programación académica.

**Especificaciones de Entregable:**

* Crear un nuevo Jupyter Notebook en **Google Colab**.
* Responder las preguntas asignadas en inglés haciendo uso de celdas de texto en formato **Markdown**.
* Sincronizar y guardar una copia del cuaderno en su cuenta personal de **GitHub** o mediante **GitHub Classroom**.
* Enviar el enlace directo al repositorio correspondiente.

**Cuestionario de Control (Markdown / Inglés):**

* **Q1: The Problem with Traditional Saving**
According to the author, why is the traditional method of saving files (e.g., `draft_1.doc`, `final_draft.doc`) problematic for scientific research, and what fundamental solution does a Version Control System (VCS) provide?


* **Q2: Collaboration and Transparency**
The article lists several "Use cases for Git in science". Choose two of these use cases (e.g., *Lab notebook*, *Backup and failsafe*, *Mechanism to solicit feedback*) and briefly explain how Git improves that specific aspect of scientific work.


* **Q3: The Power of Branching**
Briefly explain the concept of "branching" in Git. Why is this feature particularly useful for researchers who want to test a new statistical method or a new simulation algorithm?



---

### Fase 2: Sesión SOLE en Clase (El Debate Físico)

Espacio presencial de 1 hora estructurado bajo la metodología SOLE (*Self Organized Learning Environment*) estipulada para la materia.

| Etapa | Tiempo | Dinámica de Trabajo |
| --- | --- | --- |
| **Planteamiento** | 5 min

 | Presentación del caso provocador por parte del docente:

<br>

<br> "Basados en la lectura de Karthik Ram, imaginen que un equipo de físicos descubre una nueva partícula, pero pierde el financiamiento porque no usaron control de versiones. ¿Cómo estructurarían ustedes el flujo de trabajo (workflow) usando Git y GitHub para garantizar que los datos, el código de simulación y el manuscrito sean 100% reproducibles y a prueba de pérdida de datos?"

 |
| **Desarrollo** | 35 min

 | Trabajo grupal mediante pizarra o notebook colaborativo. Los estudiantes modelan un *workflow* de física integrando *commit logs* como bitácoras, ramas (*branches*) para exploración y repositorios remotos.

 |
| **Exposición** | 15 min

 | Un representante seleccionado por cada equipo expone en tiempo breve la propuesta de flujo de trabajo diseñada.

 |
| **Conclusiones** | 5 min

 | Síntesis docente que vincula la importancia de la reproducibilidad con la sintaxis inicial en Python (Elementos básicos I) y ratifica a GitHub como la bitácora oficial de código durante el semestre.

 |

---

> **Alineación curricular:** Esta actividad articula el requisito de lectura en inglés, el uso de entornos en la nube (Colab y GitHub) y el desarrollo de competencias de pensamiento computacional para la resolución reproducible de problemas físicos.
> 
>

# Semana 2
# Listas en Python: Sorting

**Dataset sintético:** Los estudiantes deben construir un dataset de minimo 5 columnas y 100 datos en cada columna.

**Códigos de sorting:** Realizar códigos de searching y sorting (organización) listas en Python para poner a prueba con el dataset. **Linear Search -> Quick Sort** en la sección Python DSA en [W3schools] (https://www.w3schools.com/python/python_dsa.asp)


**Documento:** Realizar un documento en latex con el análisis de los diferentes métodos de searching y sorting. Importante incluir el análisis del la cantidad de operaciones y el time complexities cada caso.


## Semana 3
# Guía de Actividad: Simulación de Sistemas Físicos en Python
**Asignatura:** Física Computacional I  
**Tema:** Elementos Básicos de Python II (Estamentos de E/S, Estamentos de Control, Listas/Arreglos, Lazo `for`, Funciones)  
**Modalidad:** Trabajo Individual / Asignación de Proyectos Físicos  

---

## 1. Objetivos
* Aplicar los conceptos fundamentales de programación estructurada en Python a la resolución de problemas físicos básicos.
* Implementar funciones modularizadas para describir la evolución temporal de un sistema dinámico.
* Manipular listas y arreglos para almacenar y procesar datos computados a lo largo del tiempo.
* Aplicar estamentos de control para validar parámetros de entrada y detectar eventos o condiciones límite en la simulación.

---

## 2. Requisitos Estructurales del Código
Sin importar el tema asignado, la solución de cada estudiante debe estructurarse obligatoriamente bajo los siguientes componentes:

1. **Estamentos de Entrada y Salida (E/S):**
   * Lectura interactiva de constantes y condiciones iniciales desde la consola usando `input()`.
   * Despliegue de un resumen final estructurado con los valores clave o una tabla de evolución temporal.
2. **Funciones Customizadas (`def`):**
   * Al menos una función que calcule el estado del sistema o sus derivadas en un instante de tiempo determinado.
3. **Estamentos de Control (`if` / `elif` / `else`):**
   * Validación de entradas (evitar valores no físicos como masas negativas, ángulos fuera de rango $0^\circ \le \theta \le 90^\circ$, o constantes nulas/negativas).
   * Evaluación de condiciones de parada o marcado de eventos (p. ej., impacto con el suelo, alcance del equilibrio, energía máxima).
4. **Listas y Arreglos:**
   * Uso de listas nativas de Python o arreglos de NumPy para almacenar el historial temporal del sistema (tiempo, posición, velocidad, energía, etc.).
5. **Lazo `for`:**
   * Iteración numérica sobre un rango de pasos discretos de tiempo ($\Delta t$) para actualizar y almacenar las variables del sistema.

---

## 3. Asignación de Proyectos por Estudiante

---

### **Estudiante 1: Caída libre con resistencia del aire**
* **Descripción del problema:** Simular el movimiento unidireccional de un cuerpo cayendo verticalmente bajo la influencia de la gravedad y la resistencia del aire lineal ($F_{arrastre} = -kv$).
* **Requerimientos específicos:**
  * Solicitar la masa $m$, la altura inicial $y_0$, el coeficiente $k$ y el intervalo de tiempo $\Delta t$.
  * Implementar una función para la aceleración neta: $a(v) = -g + \frac{k}{m}v$.
  * Usar un bucle `for` para actualizar iterativamente $v(t)$ e $y(t)$ guardando el historial en listas.
  * Usar condicionales `if` para detener la simulación si $y(t) \le 0$ (impacto contra el suelo) e indicar la velocidad terminal alcanzada.

---

### **Estudiante 2: Oscilador Armónico Simple (Masa-Resorte)**
* **Descripción del problema:** Determinar la evolución temporal de la posición, velocidad y energías (cinética, potencial y total) de un sistema masa-resorte no amortiguado.
* **Requerimientos específicos:**
  * Solicitar la masa $m$, la constante elástica $k$, la amplitud $A$ y el tiempo total de simulación $T$.
  * Definir funciones para calcular $x(t) = A\cos(\omega t)$, $v(t) = -A\omega\sin(\omega t)$ y la energía total $E(t) = \frac{1}{2}mv^2 + \frac{1}{2}kx^2$.
  * Recorrer los pasos de tiempo con `for` y guardar los datos de $x, v, E_{cin}, E_{pot}$ en arreglos o listas.
  * Utilizar condicionales `if` para verificar la conservación de la energía total dentro de un margen de tolerancia aceptable.

---

### **Estudiante 3: Trayectoria de Tiro Parabólico 2D**
* **Descripción del problema:** Simular la trayectoria bidimensional de un proyectil en el campo gravitatorio terrestre sin resistencia del aire.
* **Requerimientos específicos:**
  * Solicitar la velocidad inicial $v_0$ y el ángulo de lanzamiento $\theta$ (en grados).
  * Construir funciones para $x(t) = v_0 \cos(\theta) t$ e $y(t) = v_0 \sin(\theta) t - \frac{1}{2}gt^2$.
  * Generar listas independientes para el tiempo $t$, componente $x$ y componente $y$ mediante un ciclo `for`.
  * Utilizar un estamento `if` para identificar e imprimir el punto exacto donde se alcanza la altura máxima $y_{máx}$ y el alcance horizontal máximo $R$.

---

### **Estudiante 4: Ley de Enfriamiento de Newton**
* **Descripción del problema:** Modelar la pérdida/ganancia de temperatura de un objeto expuesto a un medio ambiente a temperatura constante.
* **Requerimientos específicos:**
  * Solicitar la temperatura inicial del cuerpo $T_0$, la temperatura ambiental $T_{amb}$, la constante de enfriamiento $r$ y el paso del tiempo $\Delta t$.
  * Definir una función $T(t) = T_{amb} + (T_0 - T_{amb})e^{-rt}$ o su versión iterativa $\Delta T = -r(T - T_{amb})\Delta t$.
  * Guardar el historial de tiempo y temperatura en listas a lo largo de $N$ pasos en un lazo `for`.
  * Usar condicionales `if` para detectar e imprimir cuándo la diferencia $\vert{}T(t) - T_{amb}\vert{}$ sea menor a $0.1^\circ\text{C}$ (criterio de equilibrio térmico).

---

### **Estudiante 5: Carga y Descarga de un Circuito RC**
* **Descripción del problema:** Analizar la respuesta temporal del voltaje y la corriente en un capacitor dentro de un circuito serie RC.
* **Requerimientos específicos:**
  * Solicitar la resistencia $R$, capacitancia $C$, voltaje de la fuente $V_0$ y el modo de operación (`1` para Carga, `2` para Descarga).
  * Definir funciones separadas para el voltaje en el capacitor $V_c(t)$ y la corriente $I(t)$ según el modo seleccionado.
  * Usar un lazo `for` para llenar listas/arreglos con los valores de tiempo $t$, $V_c(t)$ e $I(t)$ durante un periodo de $5\tau$ (donde $\tau = RC$).
  * Emplear estamentos `if/elif` para seleccionar las ecuaciones correspondientes y para advertir si el capacitor ha alcanzado más del $99\%$ de su carga/descarga final.

---

## 4. Criterios de Evaluación

| Criterio | Descripción | Puntaje |
| :--- | :--- | :---: |
| **Manejo de Entrada/Salida** | Validación de tipos de datos, interacción clara mediante la consola e impresiones comprensibles. | 15% |
| **Estructuras de Control** | Implementación correcta de `if/else` para manejo de errores físicos y detección de condiciones límite. | 20% |
| **Uso de Listas/Arreglos** | Correcto almacenamiento y estructura de las variables dinámicas de la simulación. | 20% |
| **Lazos Iterativos (`for`)** | Implementación adecuada del ciclo de tiempo y cálculo correcto en cada paso. | 20% |
| **Modularidad (Funciones)** | Creación de funciones reutilizables con parámetros claros y retorno adecuado de valores. | 15% |
| **Documentación y Limpieza** | Uso de comentarios claros, nombres de variables representativos y formato ordenado. | 10% |
