"""
main.py
Simulación de 12 operaciones del sistema Software FJ (válidas e inválidas).
Ejecutar con:  python main.py
"""
from sistema import SistemaFJ
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from logger import log, ARCHIVO_LOG


def titulo(texto):
    print(f"\n{texto}")


def main():
    log.info("========== INICIO DE LA SIMULACIÓN SOFTWARE FJ ==========")
    fj = SistemaFJ()

    titulo("1) Cliente válido")
    ana = fj.registrar_cliente(nombre="ana maría pérez", documento="1020304050",
                               correo="ana.perez@correo.com", telefono="3101234567")

    titulo("2) Cliente inválido (correo mal escrito)")
    fj.registrar_cliente(nombre="Carlos Ruiz", documento="9876543210",
                         correo="carlos-correo.com", telefono="3109876543")

    titulo("3) Cliente inválido (falta el documento)")
    fj.registrar_cliente(nombre="Luis Gómez", correo="luis@correo.com", telefono="3001112233")

    titulo("4) Cliente válido")
    jhon = fj.registrar_cliente(nombre="Jhon Fredy Roa", documento="80123456",
                                correo="jhon.roa@correo.com", telefono="3205556677")

    titulo("5) Servicio válido: sala de reuniones")
    sala = fj.registrar_servicio(ReservaSala, nombre="Sala Ejecutiva", tarifa_hora=50000, capacidad=25)

    titulo("6) Servicio inválido: tarifa que no es número")
    fj.registrar_servicio(AlquilerEquipo, nombre="Portátil", tarifa_hora="gratis", tipo_equipo="Laptop")

    titulo("7) Servicio válido: alquiler de equipo")
    equipo = fj.registrar_servicio(AlquilerEquipo, nombre="Video Beam", tarifa_hora=20000,
                                   tipo_equipo="Proyector", seguro=10000)

    titulo("8) Servicio válido: asesoría")
    asesoria = fj.registrar_servicio(Asesoria, nombre="Asesoría en Python", tarifa_hora=80000,
                                     especialidad="Programación", nivel="senior")

    titulo("9) Servicio inválido: nivel de asesoría que no existe")
    fj.registrar_servicio(Asesoria, nombre="Asesoría Cloud", tarifa_hora=90000,
                          especialidad="Nube", nivel="maestro")

    titulo("10) Reserva exitosa: confirmar y procesar con impuesto y descuento")
    r1 = fj.crear_reserva(ana, sala, 3)
    fj.confirmar_reserva(r1)
    fj.procesar_reserva(r1, impuesto=0.19, descuento=0.10)

    titulo("11) Reserva fallida: horas inválidas")
    fj.crear_reserva(jhon, equipo, -2)

    titulo("12) Reserva fallida: servicio no disponible")
    equipo.marcar_disponible(False)
    fj.crear_reserva(jhon, equipo, 2)
    equipo.marcar_disponible(True)

    titulo("13) Reserva fallida: cliente que no existe (None)")
    fj.crear_reserva(None, asesoria, 2)

    titulo("14) Operación no permitida: procesar sin confirmar")
    r2 = fj.crear_reserva(jhon, asesoria, 2)
    fj.procesar_reserva(r2)

    titulo("15) Cancelar y luego intentar confirmar la misma reserva")
    fj.cancelar_reserva(r2)
    fj.confirmar_reserva(r2)

    titulo("16) Cálculo inconsistente: impuesto fuera de rango (encadenamiento de excepciones)")
    r3 = fj.crear_reserva(ana, equipo, 4)
    fj.confirmar_reserva(r3)
    fj.procesar_reserva(r3, impuesto=5)
    fj.procesar_reserva(r3, impuesto=0.19)  # ahora sí, sin errores

    fj.resumen()
    log.info("========== FIN DE LA SIMULACIÓN (el sistema nunca se detuvo) ==========")
    print(f"\nLog guardado en: {ARCHIVO_LOG}")


if __name__ == "__main__":
    main()
