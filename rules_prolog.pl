%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% CONEXION

:- use_module(library(odbc)).

% Conectarse a la base de datos
connect_db(Connection) :-
    odbc_connect('tu_origen_de_datos_ODBC', Connection, [user('tu_usuario'), password('tu_contraseña'), alias(my_db), open(once)]).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% HOTELES

% Regla para obtener los hoteles
get_hoteles :- 
    connect_db(Connection),               % Conectar a la base de datos
    get_hoteles_conn(Connection),          % Llamar a la regla para obtener hoteles
    close_db(Connection).                 % Cerrar la conexión

% Obtener todos los hoteles, iterando sobre los resultados
get_hoteles_conn(Connection) :-
    odbc_query(Connection, 'SELECT * FROM "HOTELES" ORDER BY id ASC', Row_Hotel, [types([integer, atom])]),
    process_row_hotel(Row_Hotel),                    % Procesar cada fila obtenida
    fail.                                % Continuar obteniendo mas filas

get_hoteles_conn(_) :- !.                % Terminar si ya no hay mas filas

% Obtener un hotel por su ID
get_hotel_by_id(Id) :-
    connect_db(Connection),                % Conectar a la base de datos
    format('Consultando hotel con ID: ~w~n', [Id]),
    get_hotel_by_id_conn(Connection, Id),  % Llamar a la regla para obtener el hotel por ID
    close_db(Connection).                  % Cerrar la conexión

% Obtener un hotel por su ID usando odbc_prepare y odbc_execute
get_hotel_by_id_conn(Connection, Id) :-
    odbc_prepare(Connection,
                 'SELECT * FROM "HOTELES" WHERE id = ?',
                 [integer],                % Definir el tipo del parámetro
                 Statement),               % Guardar el statement preparado
    odbc_execute(Statement, [Id], Row_Hotel),    % Ejecutar la consulta con el parámetro
    process_row_hotel(Row_Hotel),                      % Procesar la fila obtenida
    odbc_free_statement(Statement).        % Liberar el statement preparado

% Procesar cada fila obtenida
process_row_hotel(row(Id, Nombre)) :-
    format('~w, ~w~n', [Id, Nombre]).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% DUEÑOS

% Regla para obtener los dueños
get_dueños :- 
    connect_db(Connection),               % Conectar a la base de datos
    get_dueños_conn(Connection),          % Llamar a la regla para obtener dueños
    close_db(Connection).                 % Cerrar la conexión

% Obtener todos los dueños, iterando sobre los resultados
get_dueños_conn(Connection) :-
    odbc_query(Connection, 'SELECT * FROM "DUEÑOS" ORDER BY id ASC', Row_Dueño, [types([integer, atom, atom, atom, atom])]),
    process_row_dueño(Row_Dueño),                    % Procesar cada fila obtenida
    fail.

get_dueños_conn(_) :- !.               

get_dueño_by_id(Id) :-
    connect_db(Connection),                % Conectar a la base de datos
    format('Consultando dueño con ID: ~w~n', [Id]),
    get_dueño_by_id_conn(Connection, Id),  % Llamar a la regla para obtener por id
    close_db(Connection).                  % Cerrar la conexión

get_dueño_by_id_conn(Connection, Id) :-
    odbc_prepare(Connection,
                 'SELECT * FROM "DUEÑOS" WHERE id = ?',
                 [integer],                % Definir el tipo del parámetro
                 Statement),               % Guardar el statement preparado
    odbc_execute(Statement, [Id], Row_Dueño),    % Ejecutar la consulta con el parámetro
    process_row_dueño(Row_Dueño),                      % Procesar la fila obtenida
    odbc_free_statement(Statement).        % Liberar el statement preparado

process_row_dueño(row(Id, Nombre, Telefono, Email, Estado)) :-
    format('~w, ~w, ~w, ~w, ~w~n', [Id, Nombre, Telefono, Email, Estado]).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% CUARTOS

% Regla para obtener los cuartos
get_cuartos :- 
    connect_db(Connection),               % Conectar a la base de datos
    get_cuartos_conn(Connection),          % Llamar a la regla para obtener dueños
    close_db(Connection).                 % Cerrar la conexión

% Obtener todos los cuartos, iterando sobre los resultados
get_cuartos_conn(Connection) :-
    odbc_query(Connection, 'SELECT * FROM "CUARTOS" ORDER BY id ASC', Row_Cuarto, [types([integer, integer, integer, atom])]),
    process_row_cuarto(Row_Cuarto),                    % Procesar cada fila obtenida
    fail.

get_cuartos_conn(_) :- !.               

get_cuarto_by_id(Id) :-
    connect_db(Connection),                % Conectar a la base de datos
    format('Consultando cuarto con ID: ~w~n', [Id]),
    get_cuarto_by_id_conn(Connection, Id),  % Llamar a la regla para obtener por id
    close_db(Connection).                  % Cerrar la conexión

get_cuarto_by_id_conn(Connection, Id) :-
    odbc_prepare(Connection,
                 'SELECT * FROM "CUARTOS" WHERE id = ?',
                 [integer],                % Definir el tipo del parámetro
                 Statement),               % Guardar el statement preparado
    odbc_execute(Statement, [Id], Row_Cuarto),    % Ejecutar la consulta con el parámetro
    process_row_cuarto(Row_Cuarto),                      % Procesar la fila obtenida
    odbc_free_statement(Statement).        % Liberar el statement preparado

get_cuartos_disponibles :- 
    connect_db(Connection),               % Conectar a la base de datos
    get_cuartos_disponibles_conn(Connection),          % Llamar a la regla para obtener dueños
    close_db(Connection).                 % Cerrar la conexión

% Obtener todos los dueños, iterando sobre los resultados
get_cuartos_disponibles_conn(Connection) :-
    odbc_query(Connection, 'SELECT * FROM "CUARTOS" WHERE disponible = true ORDER BY id ASC', Row_Cuarto, [types([integer, integer, integer, atom])]),
    process_row_cuarto(Row_Cuarto),                    % Procesar cada fila obtenida
    fail.

get_cuartos_disponibles_conn(_) :- !.  

process_row_cuarto(row(Id, Id_Hotel, Numero_Cuarto, Disponible)) :-
    format('~w, ~w, ~w, ~w~n', [Id, Id_Hotel, Numero_Cuarto, Disponible]).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% MASCOTAS
get_mascotas :- 
    connect_db(Connection),               % Conectar a la base de datos
    get_mascotas_conn(Connection),          % Llamar a la regla para obtener dueños
    close_db(Connection).                 % Cerrar la conexión

% Obtener todas las mascotas, iterando sobre los resultados
get_mascotas_conn(Connection) :-
    odbc_query(Connection, 'SELECT * FROM "MASCOTAS" ORDER BY id ASC', Row_Mascota, [types([integer, atom, atom, atom, atom, float, integer, atom])]),
    process_row_mascota(Row_Mascota),                    % Procesar cada fila obtenida
    fail.

get_mascotas_conn(_) :- !.               

get_mascota_by_id(Id) :-
    connect_db(Connection),                % Conectar a la base de datos
    format('Consultando mascota con ID: ~w~n', [Id]),
    get_mascota_by_id_conn(Connection, Id),  % Llamar a la regla para obtener por id
    close_db(Connection).                  % Cerrar la conexión

get_mascota_by_id_conn(Connection, Id) :-
    odbc_prepare(Connection,
                 'SELECT * FROM "MASCOTAS" WHERE id = ?',
                 [integer],                % Definir el tipo del parámetro
                 Statement),               % Guardar el statement preparado
    odbc_execute(Statement, [Id], Row_Mascota),    % Ejecutar la consulta con el parámetro
    process_row_mascota(Row_Mascota),                      % Procesar la fila obtenida
    odbc_free_statement(Statement).        % Liberar el statement preparado

process_row_mascota(row(Id, Nombre, Raza, Edad, Genero, Peso, Id_Dueño, Estado)) :-
    format('~w, ~w, ~w, ~w, ~w, ~w, ~w, ~w~n', [Id, Nombre, Raza, Edad, Genero, Peso, Id_Dueño, Estado]).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% DETALLES_MASCOTAS
get_detalles :- 
    connect_db(Connection),                 % Conectar a la base de datos
    get_detalles_conn(Connection),          % Llamar a la regla para obtener dueños
    close_db(Connection).                   % Cerrar la conexión

get_detalles_conn(Connection) :-
    odbc_query(Connection, 'SELECT * FROM "DETALLES_MASCOTAS" ORDER BY id ASC', Row_Detalle, [types([integer, integer, atom, atom, atom, atom, atom, float, atom])]),
    process_row_detalle(Row_Detalle),                    % Procesar cada fila obtenida
    fail.

get_detalles_conn(_) :- !.               

get_detalle_by_id(Id) :-
    connect_db(Connection),                % Conectar a la base de datos
    format('Consultando detalle con ID: ~w~n', [Id]),
    get_detalle_by_id_conn(Connection, Id),  % Llamar a la regla para obtener por id
    close_db(Connection).                  % Cerrar la conexión

get_detalle_by_id_conn(Connection, Id) :-
    odbc_prepare(Connection,
                 'SELECT * FROM "DETALLES_MASCOTAS" WHERE id = ?',
                 [integer],                % Definir el tipo del parámetro
                 Statement),               % Guardar el statement preparado
    odbc_execute(Statement, [Id], Row_Detalle),    % Ejecutar la consulta con el parámetro
    process_row_detalle(Row_Detalle),                      % Procesar la fila obtenida
    odbc_free_statement(Statement).        % Liberar el statement preparado

process_row_detalle(row(Id, Id_Mascota, Inicio_Desayuno, Fin_Desayuno, Inicio_Comida, Fin_Comida, Agresividad, Temperatura, Comentarios)) :-
    format('~w, ~w, ~w, ~w, ~w, ~w, ~w, ~w, ~w~n', [Id, Id_Mascota, Inicio_Desayuno, Fin_Desayuno, Inicio_Comida, Fin_Comida, Agresividad, Temperatura, Comentarios]).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% ESTANCIAS

get_estancias :- 
    connect_db(Connection),               % Conectar a la base de datos
    get_estancias_conn(Connection),          % Llamar a la regla para obtener dueños
    close_db(Connection).                 % Cerrar la conexión

get_estancias_conn(Connection) :-
    odbc_query(Connection, 'SELECT * FROM "ESTANCIAS" ORDER BY id ASC', Row_Estancia, [types([integer, integer, integer, atom, atom, float])]),
    process_row_estancia(Row_Estancia),                    % Procesar cada fila obtenida
    fail.

get_estancias_conn(_) :- !.               

get_estancia_by_id(Id) :-
    connect_db(Connection),                % Conectar a la base de datos
    format('Consultando estancia con ID: ~w~n', [Id]),
    get_estancia_by_id_conn(Connection, Id),  % Llamar a la regla para obtener por id
    close_db(Connection).                  % Cerrar la conexión

get_estancia_by_id_conn(Connection, Id) :-
    odbc_prepare(Connection,
                 'SELECT * FROM "ESTANCIAS" WHERE id = ?',
                 [integer],                % Definir el tipo del parámetro
                 Statement),               % Guardar el statement preparado
    odbc_execute(Statement, [Id], Row_Estancia),    % Ejecutar la consulta con el parámetro
    process_row_estancia(Row_Estancia),                      % Procesar la fila obtenida
    odbc_free_statement(Statement).        % Liberar el statement preparado

process_row_estancia(row(Id, Id_Detalle, Id_Cuarto, Inicio_Estancia, Fin_Estancia, Importe)) :-
    format('~w, ~w, ~w, ~w, ~w, ~w~n', [Id, Id_Detalle, Id_Cuarto, Inicio_Estancia, Fin_Estancia, Importe]).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% REGLAS ESPECIALES

% Regla para verificar si es hora de alimentar a la mascota
es_hora_de_alimentar(IdMascota, HoraActual) :-
    % Conectar a la base de datos
    connect_db(Connection),
    % Preparar y ejecutar la consulta
    odbc_prepare(Connection, 
                 'SELECT inicio_desayuno, fin_desayuno, inicio_comida, fin_comida FROM "DETALLES_MASCOTAS" WHERE id = ?', 
                 [integer], 
                 Statement),
    odbc_execute(Statement, [IdMascota], row(InicioDesayuno, FinDesayuno, InicioComida, FinComida)),

    % Convertir HoraActual a minutos
    split_string(HoraActual, ":", "", [HStr, MStr]),
    atom_number(HStr, Hora),
    atom_number(MStr, Minuto),
    MinutosActual is Hora * 60 + Minuto,

    % Convertir los horarios a minutos
    split_string(InicioDesayuno, ":", "", [HDStart, MDStart]),
    atom_number(HDStart, HoraInicioDesayuno),
    atom_number(MDStart, MinutoInicioDesayuno),
    MinutosInicioDesayuno is HoraInicioDesayuno * 60 + MinutoInicioDesayuno,

    split_string(FinDesayuno, ":", "", [HDEnd, MDEnd]),
    atom_number(HDEnd, HoraFinDesayuno),
    atom_number(MDEnd, MinutoFinDesayuno),
    MinutosFinDesayuno is HoraFinDesayuno * 60 + MinutoFinDesayuno,

    split_string(InicioComida, ":", "", [HCStart, MCStart]),
    atom_number(HCStart, HoraInicioComida),
    atom_number(MCStart, MinutoInicioComida),
    MinutosInicioComida is HoraInicioComida * 60 + MinutoInicioComida,

    split_string(FinComida, ":", "", [HCEnd, MCEnd]),
    atom_number(HCEnd, HoraFinComida),
    atom_number(MCEnd, MinutoFinComida),
    MinutosFinComida is HoraFinComida * 60 + MinutoFinComida,

    % Verificar si la hora actual está dentro de los horarios
    (   (MinutosActual >= MinutosInicioDesayuno, MinutosActual =< MinutosFinDesayuno)
    ->  format("true")
    ;   (MinutosActual >= MinutosInicioComida, MinutosActual =< MinutosFinComida)
    ->  format("true")
    ;   format("false")
    ),
    
    % Liberar el statement y cerrar la conexión
    odbc_free_statement(Statement),
    close_db(Connection).

regular_temperatura(TemperaturaActual, IdMascota) :-
    connect_db(Connection),
    odbc_prepare(Connection,
                 'SELECT temperatura_ideal FROM "DETALLES_MASCOTAS" WHERE id = ?',
                 [integer],
                 Statement),
    odbc_execute(Statement, [IdMascota], row(TemperaturaOptima)),
    odbc_free_statement(Statement),
    close_db(Connection),
    (   TemperaturaActual >= TemperaturaOptima
    ->  format('true~n')
    ;   format('false~n')
    ).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% CERRAR CONEXIÓN

% Cerrar conexión
close_db(Connection) :-
    odbc_disconnect(Connection).
