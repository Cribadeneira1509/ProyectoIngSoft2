import pytest
from logica import Login, Usuario, Servicio, Reserva, Pago, HistorialReservas

def test_usuario_registro_exitoso(mocker):
    mock_executor = mocker.MagicMock(return_value=True)

    data = {
        "email": "nuevo@test.com",
        "password": "Password123",
        "firstName": "Carlos",
        "lastName": "R",
        "identificationId": "123456"
    }

    mocker.patch("logica.Usuario.existe_en_bd", return_value=False)
    mocker.patch("logica.send_email_notification", return_value=True)

    usuario = Usuario(data, mock_executor)
    resultado = usuario.registrar()

    assert resultado["success"] is True
    mock_executor.assert_called()

def test_usuario_registro_duplicado(mocker):
    mock_executor = mocker.MagicMock()

    data = {
        "email": "existente@test.com",
        "password": "Password123",
        "firstName": "Carlos",
        "lastName": "R",
        "identificationId": "123456"
    }

    mocker.patch("logica.Usuario.existe_en_bd", return_value=True)

    usuario = Usuario(data, mock_executor)
    resultado = usuario.registrar()

    assert resultado["success"] is False
    assert "ya está registrado" in resultado["message"]

def test_usuario_password_corta(mocker):
    mock_executor = mocker.MagicMock()

    data = {
        "email": "test@test.com",
        "password": "123",
        "firstName": "Carlos",
        "lastName": "R",
        "identificationId": "123456"
    }

    mocker.patch("logica.Usuario.existe_en_bd", return_value=False)

    usuario = Usuario(data, mock_executor)
    resultado = usuario.registrar()

    assert resultado["success"] is False

def test_login_exitoso(mocker):
    mock_executor = mocker.MagicMock(return_value=(
        "1", "Carlos", "1234", "Cliente",
        "test@test.com", "Carlos", "R", "123456"
    ))

    login = Login("test@test.com", "1234", mock_executor)
    resultado = login.autenticar()

    assert resultado["success"] is True
    assert resultado["isAdmin"] is False

def test_login_correo_invalido(mocker):
    mock_executor = mocker.MagicMock()

    login = Login("correo-malo", "1234", mock_executor)
    resultado = login.autenticar()

    assert resultado["success"] is False
    assert "Correo inválido" in resultado["message"]

def test_login_password_incorrecta(mocker):
    mock_executor = mocker.MagicMock(return_value=(
        "1", "Carlos", "correcta", "Cliente",
        "test@test.com", "Carlos", "R", "123456"
    ))

    login = Login("test@test.com", "incorrecta", mock_executor)
    resultado = login.autenticar()

    assert resultado["success"] is False

def test_obtener_servicios_vacio(mocker):
    mock_executor = mocker.MagicMock(return_value=None)

    servicio = Servicio(None, mock_executor)
    resultado = servicio.obtener_todos()

    assert resultado["success"] is True
    assert resultado["data"] == []

def test_crear_servicio_exitoso(mocker):
    mock_executor = mocker.MagicMock(return_value=True)

    data = {
        "providerId": "prov1",
        "expertName": "Experto",
        "name": "Consulta",
        "price": 20,
        "duration": 30,
        "capacity": 1,
        "modality": "Online",
        "desc": "Consulta general"
    }

    servicio = Servicio(data, mock_executor)
    resultado = servicio.crear()

    assert resultado["success"] is True

def test_crear_reserva_exitosa(mocker):
    mock_executor = mocker.MagicMock(return_value=True)
    mocker.patch("logica.send_email_notification", return_value=True)

    data = {
        "usuarioId": "u1",
        "serviceId": "s1",
        "slotTime": "2025-12-31 15:00:00",
        "status": "BLOQUEADO",
        "userEmail": "test@test.com",
        "serviceName": "Consulta"
    }

    reserva = Reserva(data, mock_executor)
    resultado = reserva.crear_reserva()

    assert resultado["success"] is True

def test_reserva_fecha_invalida(mocker):
    mock_executor = mocker.MagicMock()

    data = {
        "usuarioId": "u1",
        "serviceId": "s1",
        "slotTime": "fecha-mala",
        "status": "BLOQUEADO",
        "userEmail": "test@test.com",
        "serviceName": "Consulta"
    }

    reserva = Reserva(data, mock_executor)
    resultado = reserva.crear_reserva()

    assert resultado["success"] is False

def test_pago_online_exitoso(mocker):
    mock_executor = mocker.MagicMock(return_value=True)

    data = {
        "metodo": "online",
        "monto": 50,
        "reserva_id": "r1"
    }

    pago = Pago(data, mock_executor)
    resultado = pago.procesar_pago()

    assert resultado["success"] is True
    assert resultado["estado_pago"] == "APROBADO"

def test_pago_metodo_invalido(mocker):
    mock_executor = mocker.MagicMock()

    data = {
        "metodo": "bitcoin",
        "monto": 50,
        "reserva_id": "r1"
    }

    pago = Pago(data, mock_executor)
    resultado = pago.procesar_pago()

    assert resultado["success"] is False
