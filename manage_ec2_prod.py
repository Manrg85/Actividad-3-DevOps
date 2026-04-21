import boto3

# ─── Datos del alumno ───────────────────────────────────────────
ALUMNO    = "Manuel"
MATRICULA = "03029008"
AMBIENTE  = "Producción"
REGION    = "us-east-1"

# ─── Filtro: solo instancias del ambiente Production ────────────
FILTROS = [
    {"Name": "tag:Environment", "Values": ["Production"]},
    {"Name": "tag:Owner",       "Values": [MATRICULA]}
]

ec2 = boto3.client("ec2", region_name=REGION)

def mostrar_menu():
    print("\n" + "="*40)
    print(f"  Alumno:    {ALUMNO}")
    print(f"  Matrícula: {MATRICULA}")
    print(f"  Ambiente:  {AMBIENTE}")
    print("="*40)
    print("  1. Listar instancias")
    print("  2. Iniciar instancia")
    print("  3. Detener instancia")
    print("  4. Reiniciar instancia")
    print("  5. Salir")
    print("="*40)

def listar_instancias():
    response = ec2.describe_instances(Filters=FILTROS)
    instancias = []
    for reservation in response["Reservations"]:
        for inst in reservation["Instances"]:
            nombre = next(
                (t["Value"] for t in inst.get("Tags", []) if t["Key"] == "Name"),
                "Sin nombre"
            )
            instancias.append({
                "nombre":  nombre,
                "id":      inst["InstanceId"],
                "estado":  inst["State"]["Name"],
                "ip_priv": inst.get("PrivateIpAddress", "N/A"),
                "ip_pub":  inst.get("PublicIpAddress",  "N/A")
            })

    if not instancias:
        print("\n⚠️  No se encontraron instancias.")
        return instancias

    print(f"\n{'#':<3} {'Nombre':<25} {'ID':<20} {'Estado':<12} {'IP Privada':<16} {'IP Pública'}")
    print("-" * 90)
    for i, inst in enumerate(instancias, 1):
        print(f"{i:<3} {inst['nombre']:<25} {inst['id']:<20} {inst['estado']:<12} {inst['ip_priv']:<16} {inst['ip_pub']}")
    return instancias

def seleccionar_instancia(instancias):
    try:
        opcion = int(input("\nNúmero de instancia: "))
        if 1 <= opcion <= len(instancias):
            return instancias[opcion - 1]
    except ValueError:
        pass
    print("Opción inválida.")
    return None

def iniciar_instancia():
    instancias = listar_instancias()
    inst = seleccionar_instancia(instancias)
    if inst:
        ec2.start_instances(InstanceIds=[inst["id"]])
        print(f"\n✅ Instancia {inst['nombre']} iniciada.")

def detener_instancia():
    instancias = listar_instancias()
    inst = seleccionar_instancia(instancias)
    if inst:
        ec2.stop_instances(InstanceIds=[inst["id"]])
        print(f"\n✅ Instancia {inst['nombre']} detenida.")

def reiniciar_instancia():
    instancias = listar_instancias()
    inst = seleccionar_instancia(instancias)
    if inst:
        ec2.reboot_instances(InstanceIds=[inst["id"]])
        print(f"\n✅ Instancia {inst['nombre']} reiniciada.")

# ─── Main loop ──────────────────────────────────────────────────
while True:
    mostrar_menu()
    opcion = input("Seleccione una opción: ").strip()

    if   opcion == "1": listar_instancias()
    elif opcion == "2": iniciar_instancia()
    elif opcion == "3": detener_instancia()
    elif opcion == "4": reiniciar_instancia()
    elif opcion == "5":
        print("\nHasta luego!\n")
        break
    else:
        print("\n⚠️  Opción no válida.")