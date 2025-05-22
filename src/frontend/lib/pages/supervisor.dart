import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter/services.dart';
import '../config/config.dart';

class SupervisorDashboard extends StatefulWidget {
  final String token;

  const SupervisorDashboard({Key? key, required this.token}) : super(key: key);

  static const primaryColor = Color(0xFF1A73E8); // Blue
  static const secondaryColor = Color(0xFF34A853); // Green accent
  static const accentColor = Color(0xFFFBBC05); // Yellow accent
  static const warningColor = Color(0xFFEA4335); // Red for alerts
  static const backgroundColor = Colors.white;
  static const cardColor = Color(0xFFF8F9FA); // Light gray/white

  @override
  State<SupervisorDashboard> createState() => _SupervisorDashboardState();
}

class _SupervisorDashboardState extends State<SupervisorDashboard> {
  String selectedSection = 'dashboard';

  // Microservicios
  Future<List<dynamic>> fetchShifts() async {
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/shifts/'),
      headers: {
        'Authorization': 'Bearer ${widget.token}',
        'accept': 'application/json',
      },
    );
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Error al cargar turnos');
    }
  }

  Future<Map<String, dynamic>> fetchReport() async {
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/reporte/supervisor'),
      headers: {
        'Authorization': 'Bearer ${widget.token}',
        'accept': 'application/json',
      },
    );
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Error al cargar reporte');
    }
  }

  Future<List<dynamic>> fetchTransportUnits() async {
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/transport_units/'),
      headers: {
        'Authorization': 'Bearer ${widget.token}',
        'accept': 'application/json',
      },
    );
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Error al cargar unidades');
    }
  }

  Future<List<dynamic>> fetchIncidences() async {
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/incidences/'),
      headers: {
        'Authorization': 'Bearer ${widget.token}',
        'accept': 'application/json',
      },
    );
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Error al cargar incidencias');
    }
  }

  Future<Map<String, dynamic>> fetchDashboardData() async {
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/login/dashboard'),
      headers: {
        'Authorization': 'Bearer ${widget.token}',
        'accept': 'application/json',
      },
    );
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Error al cargar datos del dashboard');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        elevation: 0,
        backgroundColor: SupervisorDashboard.primaryColor,
        title: const Text(
          'Panel de Supervisor',
          style: TextStyle(
            fontWeight: FontWeight.w600,
            fontSize: 20,
          ),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications_outlined),
            onPressed: () {},
            tooltip: 'Notificaciones',
          ),
          IconButton(
            icon: const Icon(Icons.settings_outlined),
            onPressed: () {},
            tooltip: 'Configuración',
          ),
          IconButton(
            icon: const Icon(Icons.account_circle_outlined),
            onPressed: () {},
            tooltip: 'Perfil',
          ),
        ],
        systemOverlayStyle: SystemUiOverlayStyle.light,
      ),
      body: Row(
        children: [
          // Sidebar
          Container(
            width: 250,
            color: const Color(0xFFF8F9FA),
            child: Column(
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(
                      vertical: 24, horizontal: 16),
                  color: SupervisorDashboard.primaryColor.withOpacity(0.05),
                  child: Row(
                    children: [
                      CircleAvatar(
                        backgroundColor: SupervisorDashboard.accentColor,
                        radius: 24,
                        child: const Text(
                          'S',
                          style: TextStyle(
                            color: Color(0xFF202124),
                            fontWeight: FontWeight.bold,
                            fontSize: 18,
                          ),
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text(
                              'Supervisor',
                              style: TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 16,
                                color: Color(0xFF202124),
                              ),
                              overflow: TextOverflow.ellipsis,
                            ),
                            const SizedBox(height: 4),
                            Container(
                              padding: const EdgeInsets.symmetric(
                                  horizontal: 8, vertical: 2),
                              decoration: BoxDecoration(
                                color: SupervisorDashboard.accentColor,
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: const Text(
                                'Supervisor',
                                style: TextStyle(
                                  color: Color(0xFF202124),
                                  fontSize: 12,
                                  fontWeight: FontWeight.w500,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
                const Divider(height: 1),
                Expanded(
                  child: ListView(
                    padding: EdgeInsets.zero,
                    children: [
                      _buildMenuItem(
                        icon: Icons.dashboard_outlined,
                        title: 'Panel Principal',
                        color: SupervisorDashboard.primaryColor,
                        isActive: selectedSection == 'dashboard',
                        onTap: () {
                          setState(() {
                            selectedSection = 'dashboard';
                          });
                        },
                      ),
                      _buildMenuItem(
                        icon: Icons.schedule_outlined,
                        title: 'Asignar Turnos',
                        color: SupervisorDashboard.primaryColor,
                        isActive: selectedSection == 'shifts',
                        onTap: () {
                          setState(() {
                            selectedSection = 'shifts';
                          });
                        },
                      ),
                      _buildMenuItem(
                        icon: Icons.assessment_outlined,
                        title: 'Reporte de desempeño',
                        color: SupervisorDashboard.primaryColor,
                        isActive: selectedSection == 'report',
                        onTap: () {
                          setState(() {
                            selectedSection = 'report';
                          });
                        },
                      ),
                      _buildMenuItem(
                        icon: Icons.directions_bus_outlined,
                        title: 'Obtener Información de Unidad',
                        color: SupervisorDashboard.primaryColor,
                        isActive: selectedSection == 'units',
                        onTap: () {
                          setState(() {
                            selectedSection = 'units';
                          });
                        },
                      ),
                      _buildMenuItem(
                        icon: Icons.warning_amber_outlined,
                        title: 'Consultar Incidencias',
                        color: SupervisorDashboard.primaryColor,
                        isActive: selectedSection == 'incidences',
                        onTap: () {
                          setState(() {
                            selectedSection = 'incidences';
                          });
                        },
                      ),
                    ],
                  ),
                ),
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(16),
                  child: ElevatedButton.icon(
                    onPressed: () {},
                    icon: const Icon(Icons.logout, size: 18),
                    label: const Text('Cerrar Sesión'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.white,
                      foregroundColor: SupervisorDashboard.primaryColor,
                      elevation: 0,
                      padding: const EdgeInsets.symmetric(vertical: 12),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(8),
                        side: BorderSide(
                            color: SupervisorDashboard.primaryColor),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
          // Main content
          Expanded(
            child: Container(
              color: const Color(0xFFF5F7FA),
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(24),
                child: _buildSectionContent(),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSectionContent() {
    switch (selectedSection) {
      case 'shifts':
        return FutureBuilder<List<dynamic>>(
          future: fetchShifts(),
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return _loadingWidget('Cargando turnos...');
            } else if (snapshot.hasError) {
              return _errorWidget('Error al cargar turnos');
            } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
              return _emptyWidget('No hay turnos disponibles.');
            }
            final shifts = snapshot.data!;
            return Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Turnos Asignados',
                    style:
                        TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                const SizedBox(height: 24),
                DataTable(
                  headingRowColor: MaterialStateProperty.all(
                      SupervisorDashboard.primaryColor.withOpacity(0.1)),
                  columns: const [
                    DataColumn(label: Text('ID')),
                    DataColumn(label: Text('Tipo')),
                    DataColumn(label: Text('Inicio')),
                    DataColumn(label: Text('Fin')),
                  ],
                  rows: shifts.map((shift) {
                    return DataRow(
                      cells: [
                        DataCell(Text(shift['ID']?.toString() ?? '-')),
                        DataCell(Text(shift['TipoTurno']?.toString() ?? '-')),
                        DataCell(Text(shift['HoraInicio']?.toString() ?? '-')),
                        DataCell(Text(shift['HoraFin']?.toString() ?? '-')),
                      ],
                    );
                  }).toList(),
                ),
              ],
            );
          },
        );
      case 'report':
        return FutureBuilder<Map<String, dynamic>>(
          future: fetchReport(),
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return _loadingWidget('Cargando reporte...');
            } else if (snapshot.hasError) {
              return _errorWidget('Error al cargar reporte');
            } else if (!snapshot.hasData) {
              return _emptyWidget('No hay datos de reporte.');
            }
            final data = snapshot.data!;
            return Card(
              elevation: 2,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(16),
              ),
              child: Padding(
                padding: const EdgeInsets.all(24.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(Icons.bar_chart,
                            color: SupervisorDashboard.primaryColor, size: 32),
                        const SizedBox(width: 12),
                        const Text('Resumen de Desempeño',
                            style: TextStyle(
                                fontSize: 20, fontWeight: FontWeight.bold)),
                      ],
                    ),
                    const SizedBox(height: 20),
                    _buildReportRow('Total de Movimientos',
                        data['total_movimientos']?.toString() ?? '-'),
                    _buildReportRow('Total de Usuarios',
                        data['total_usuarios']?.toString() ?? '-'),
                    _buildReportRow(
                        'Promedio de Horas Trabajadas',
                        data['promedio_horas_trabajadas']?.toString() ?? '-'),
                  ],
                ),
              ),
            );
          },
        );
      case 'units':
        return FutureBuilder<List<dynamic>>(
          future: fetchTransportUnits(),
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return _loadingWidget('Cargando unidades...');
            } else if (snapshot.hasError) {
              return _errorWidget('Error al cargar unidades');
            } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
              return _emptyWidget('No hay unidades disponibles.');
            }
            final units = snapshot.data!;
            return Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Unidades de Transporte',
                    style:
                        TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                const SizedBox(height: 24),
                DataTable(
                  headingRowColor: MaterialStateProperty.all(
                      SupervisorDashboard.secondaryColor.withOpacity(0.1)),
                  columns: const [
                    DataColumn(label: Text('ID')),
                    DataColumn(label: Text('Ubicación')),
                    DataColumn(label: Text('Capacidad')),
                    DataColumn(label: Text('Ruta')),
                    DataColumn(label: Text('Tipo')),
                  ],
                  rows: units.map((unit) {
                    return DataRow(
                      cells: [
                        DataCell(Text(unit['ID']?.toString() ?? '-')),
                        DataCell(Text(unit['Ubicacion']?.toString() ?? '-')),
                        DataCell(Text(unit['Capacidad']?.toString() ?? '-')),
                        DataCell(Text(unit['IDRuta']?.toString() ?? '-')),
                        DataCell(Text(unit['IDTipo']?.toString() ?? '-')),
                      ],
                    );
                  }).toList(),
                ),
              ],
            );
          },
        );
      case 'incidences':
        return FutureBuilder<List<dynamic>>(
          future: fetchIncidences(),
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return _loadingWidget('Cargando incidencias...');
            } else if (snapshot.hasError) {
              return _errorWidget('Error al cargar incidencias');
            } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
              return _emptyWidget('No hay incidencias registradas.');
            }
            final incidences = snapshot.data!;
            return Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Incidencias',
                    style:
                        TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                const SizedBox(height: 24),
                DataTable(
                  headingRowColor: MaterialStateProperty.all(
                      SupervisorDashboard.warningColor.withOpacity(0.1)),
                  columns: const [
                    DataColumn(label: Text('ID')),
                    DataColumn(label: Text('Ticket')),
                    DataColumn(label: Text('Descripción')),
                    DataColumn(label: Text('Tipo')),
                    DataColumn(label: Text('Unidad')),
                  ],
                  rows: incidences.map((inc) {
                    return DataRow(
                      cells: [
                        DataCell(Text(inc['ID']?.toString() ?? '-')),
                        DataCell(Text(inc['IDTicket']?.toString() ?? '-')),
                        DataCell(Text(inc['Descripcion']?.toString() ?? '-')),
                        DataCell(Text(inc['Tipo']?.toString() ?? '-')),
                        DataCell(Text(inc['IDUnidad']?.toString() ?? '-')),
                      ],
                    );
                  }).toList(),
                ),
              ],
            );
          },
        );
      default:
        // Dashboard principal
        return FutureBuilder<Map<String, dynamic>>(
          future: fetchDashboardData(),
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return _loadingWidget('Cargando información...');
            } else if (snapshot.hasError) {
              return _errorWidget('Error al cargar dashboard');
            } else if (!snapshot.hasData) {
              return _emptyWidget('Sin datos disponibles');
            }
            final data = snapshot.data!;
            final totalVehiculos = data['total_vehiculos'] ?? 0;
            final totalPasajeros = data['total_passanger'] ?? 0;
            final totalOperarios = data['total_operative'] ?? 0;
            return Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            const Icon(
                              Icons.supervisor_account,
                              color: SupervisorDashboard.accentColor,
                              size: 28,
                            ),
                            const SizedBox(width: 12),
                            const Text(
                              'Panel de Supervisión',
                              style: TextStyle(
                                fontSize: 24,
                                fontWeight: FontWeight.bold,
                                color: Color(0xFF202124),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'Bienvenido, Supervisor. Aquí está el resumen de tu equipo.',
                          style: const TextStyle(
                            fontSize: 16,
                            color: Color(0xFF5F6368),
                          ),
                        ),
                      ],
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 16,
                        vertical: 8,
                      ),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(
                          color: const Color(0xFFDFE1E5),
                          width: 1,
                        ),
                      ),
                      child: Row(
                        children: [
                          const Icon(
                            Icons.calendar_today,
                            size: 18,
                            color: SupervisorDashboard.accentColor,
                          ),
                          const SizedBox(width: 8),
                          Text(
                            _getCurrentDate(),
                            style: const TextStyle(
                              fontSize: 14,
                              fontWeight: FontWeight.w500,
                              color: Color(0xFF202124),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 24),
                Row(
                  children: [
                    Expanded(
                      child: _buildStatCard(
                        title: 'Solicitudes Abiertas',
                        value: '8',
                        icon: Icons.assignment,
                        color: SupervisorDashboard.primaryColor,
                        subtitle: 'Total en curso',
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: _buildStatCard(
                        title: 'Solicitudes Atrasadas',
                        value: '0',
                        icon: Icons.assignment_late,
                        color: SupervisorDashboard.warningColor,
                        subtitle: 'Sin resolver',
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: _buildStatCard(
                        title: 'Tareas Vencidas',
                        value: '7',
                        icon: Icons.assignment_turned_in,
                        color: SupervisorDashboard.accentColor,
                        subtitle: 'Supervisión requerida',
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 24),
                Row(
                  children: [
                    Expanded(
                      child: _buildChartBox(
                        title: 'Distribución por Regulación',
                        child: const Center(
                          child: Text('[Gráfico circular aquí]'),
                        ),
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: _buildChartBox(
                        title: 'Distribución por Actividad',
                        child: const Center(
                          child: Text('[Gráfico circular aquí]'),
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                _buildChartBox(
                  title: 'Solicitudes en el tiempo',
                  full: true,
                  child: const Center(
                    child: Text('[Gráfico de líneas aquí]'),
                  ),
                ),
              ],
            );
          },
        );
    }
  }

  Widget _buildMenuItem({
    required IconData icon,
    required String title,
    required Color color,
    bool isActive = false,
    VoidCallback? onTap,
  }) {
    return ListTile(
      leading: Icon(
        icon,
        color: isActive ? color : const Color(0xFF5F6368),
      ),
      title: Text(
        title,
        style: TextStyle(
          fontSize: 14,
          fontWeight: isActive ? FontWeight.w600 : FontWeight.w500,
          color: isActive ? color : const Color(0xFF202124),
        ),
      ),
      dense: true,
      horizontalTitleGap: 8,
      onTap: onTap,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8),
      ),
      tileColor: isActive ? color.withOpacity(0.1) : null,
      hoverColor: color.withOpacity(0.05),
    );
  }

  Widget _buildStatCard({
    required String title,
    required String value,
    required IconData icon,
    required Color color,
    String? subtitle,
  }) {
    return Card(
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(
          color: color.withOpacity(0.1),
          width: 1,
        ),
      ),
      color: SupervisorDashboard.cardColor,
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  title,
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w500,
                    color: color,
                  ),
                ),
                Container(
                  width: 40,
                  height: 40,
                  decoration: BoxDecoration(
                    color: color.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Icon(
                    icon,
                    color: color,
                    size: 20,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Text(
              value,
              style: const TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.bold,
                color: Color(0xFF202124),
              ),
            ),
            if (subtitle != null) ...[
              const SizedBox(height: 4),
              Text(
                subtitle,
                style: const TextStyle(
                  fontSize: 12,
                  color: Color(0xFF5F6368),
                ),
              ),
            ]
          ],
        ),
      ),
    );
  }

  Widget _buildChartBox({
    required String title,
    required Widget child,
    bool full = false,
  }) {
    return Expanded(
      flex: full ? 2 : 1,
      child: Card(
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
          side: BorderSide(
            color: SupervisorDashboard.primaryColor.withOpacity(0.05),
            width: 1,
          ),
        ),
        color: Colors.white,
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: const TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 16,
                  color: Color(0xFF202124),
                ),
              ),
              const SizedBox(height: 16),
              SizedBox(height: 120, child: child),
            ],
          ),
        ),
      ),
    );
  }

  Widget _loadingWidget(String text) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          CircularProgressIndicator(
            color: SupervisorDashboard.primaryColor,
            strokeWidth: 3,
          ),
          const SizedBox(height: 16),
          Text(
            text,
            style: const TextStyle(
              color: Color(0xFF5F6368),
              fontSize: 16,
            ),
          ),
        ],
      ),
    );
  }

  Widget _errorWidget(String text) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(
            Icons.error_outline,
            color: Colors.red,
            size: 60,
          ),
          const SizedBox(height: 16),
          Text(
            text,
            style: const TextStyle(color: Colors.red),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }

  Widget _emptyWidget(String text) {
    return Center(
      child: Text(
        text,
        style: const TextStyle(fontSize: 18),
      ),
    );
  }

  Widget _buildReportRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        children: [
          Text('$label:', style: const TextStyle(fontWeight: FontWeight.bold)),
          const SizedBox(width: 8),
          Text(value, style: const TextStyle(fontSize: 16)),
        ],
      ),
    );
  }

  String _getCurrentDate() {
    final now = DateTime.now();
    final months = [
      'Enero',
      'Febrero',
      'Marzo',
      'Abril',
      'Mayo',
      'Junio',
      'Julio',
      'Agosto',
      'Septiembre',
      'Octubre',
      'Noviembre',
      'Diciembre'
    ];
    return '${now.day} de ${months[now.month - 1]}, ${now.year}';
  }
}