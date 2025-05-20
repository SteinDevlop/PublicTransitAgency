class DashboardData {
  final Map<String, dynamic>? user;
  final String id;
  final int totalVehiculos;
  final int totalPasajeros;
  final int totalOperarios;
  final int totalSupervisores;
  final int registrosMantenimiento;
  final int busesMantenimiento;
  final String proximoMantenimiento;
  final String ultimoUsoTarjeta;
  final String turno;
  final String? typeCard;

  DashboardData({
    required this.user,
    required this.id,
    required this.totalVehiculos,
    required this.totalPasajeros,
    required this.totalOperarios,
    required this.totalSupervisores,
    required this.registrosMantenimiento,
    required this.busesMantenimiento,
    required this.proximoMantenimiento,
    required this.ultimoUsoTarjeta,
    required this.turno,
    this.typeCard,
  });

  factory DashboardData.fromJson(Map<String, dynamic> json) {
    return DashboardData(
      user: json['user'],
      id: json['id'] ?? '',
      totalVehiculos: json['total_vehiculos'] ?? 0,
      totalPasajeros: json['total_passanger'] ?? 0,
      totalOperarios: json['total_operative'] ?? 0,
      totalSupervisores: json['total_supervisors'] ?? 0,
      registrosMantenimiento: json['registros_mantenimiento'] ?? 0,
      busesMantenimiento: json['buses_mantenimiento'] ?? 0,
      proximoMantenimiento: json['proximo_mantenimiento'] ?? '',
      ultimoUsoTarjeta: json['ultimo_uso_tarjeta'] ?? '',
      turno: json['turno'] ?? '',
      typeCard: json['type_card'],
    );
  }
}