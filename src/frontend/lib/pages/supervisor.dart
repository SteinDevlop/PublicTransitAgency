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
      Uri.parse('${AppConfig.baseUrl}/transport_units/with_names'),
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

  Future<List<dynamic>> fetchUsers() async {
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/user/users'), // <-- Cambiado aquí
      headers: {'accept': 'application/json'},
    );
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Error al cargar usuarios');
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
          builder: (context, shiftsSnapshot) {
            if (shiftsSnapshot.connectionState == ConnectionState.waiting) {
              return _loadingWidget('Cargando turnos...');
            } else if (shiftsSnapshot.hasError) {
              return _errorWidget('Error al cargar turnos');
            } else if (!shiftsSnapshot.hasData || shiftsSnapshot.data!.isEmpty) {
              return _emptyWidget('No hay turnos disponibles.');
            }
            final shifts = shiftsSnapshot.data!;
            return FutureBuilder<List<dynamic>>(
              future: fetchUsers(),
              builder: (context, usersSnapshot) {
                if (usersSnapshot.connectionState == ConnectionState.waiting) {
                  return _loadingWidget('Cargando usuarios...');
                } else if (usersSnapshot.hasError) {
                  return _errorWidget('Error al cargar usuarios');
                } else if (!usersSnapshot.hasData || usersSnapshot.data!.isEmpty) {
                  return _emptyWidget('No hay usuarios disponibles.');
                }
                final usuarios = usersSnapshot.data!;
                Map<String, dynamic>? selectedUser;
                return StatefulBuilder(
                  builder: (context, setState) => Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Selecciona un usuario para cambiar su turno:',
                          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 12),
                      DropdownButton<Map<String, dynamic>>(
                        value: selectedUser,
                        hint: Text('Selecciona usuario'),
                        items: usuarios
                            .map<DropdownMenuItem<Map<String, dynamic>>>(
                              (u) => DropdownMenuItem<Map<String, dynamic>>(
                                value: u,
                                child: Text('${u['Nombre']} ${u['Apellido']}'),
                              ),
                            )
                            .toList(),
                        onChanged: (val) => setState(() => selectedUser = val),
                      ),
                      if (selectedUser != null)
                        UserShiftUpdateForm(userData: selectedUser!, shifts: shifts),
                    ],
                  ),
                );
              },
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
                    style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                const SizedBox(height: 24),
                ListView.builder(
                  shrinkWrap: true,
                  physics: NeverScrollableScrollPhysics(),
                  itemCount: units.length,
                  itemBuilder: (context, index) {
                    final unit = units[index];
                    return Card(
                      elevation: 2,
                      margin: const EdgeInsets.symmetric(vertical: 8),
                      color: SupervisorDashboard.secondaryColor.withOpacity(0.07),
                      child: ListTile(
                        leading: Icon(Icons.directions_bus, color: SupervisorDashboard.secondaryColor, size: 36),
                        title: Text('Unidad #${unit['ID'] ?? '-'}', style: TextStyle(fontWeight: FontWeight.bold)),
                        subtitle: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('Ubicación: ${unit['Ubicacion'] ?? '-'}'),
                            Text('Capacidad: ${unit['Capacidad'] ?? '-'}'),
                            Text('Ruta: ${unit['NombreRuta'] ?? '-'}'), // Cambiado
                            Text('Tipo: ${unit['NombreTipoTransporte'] ?? '-'}'), // Cambiado
                          ],
                        ),
                      ),
                    );
                  },
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
                    style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                const SizedBox(height: 24),
                ListView.builder(
                  shrinkWrap: true,
                  physics: NeverScrollableScrollPhysics(),
                  itemCount: incidences.length,
                  itemBuilder: (context, index) {
                    final inc = incidences[index];
                    return Card(
                      elevation: 3,
                      margin: const EdgeInsets.symmetric(vertical: 8),
                      color: SupervisorDashboard.warningColor.withOpacity(0.08),
                      child: ListTile(
                        leading: Icon(Icons.warning_amber_rounded, color: SupervisorDashboard.warningColor, size: 36),
                        title: Text(
                          inc['Descripcion'] ?? 'Sin descripción',
                          style: const TextStyle(fontWeight: FontWeight.bold),
                        ),
                        subtitle: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('Tipo: ${inc['Tipo'] ?? '-'}'),
                            Text('Unidad: ${inc['IDUnidad'] ?? '-'}'),
                            Text('Ticket: ${inc['IDTicket'] ?? '-'}'),
                          ],
                        ),
                        trailing: Text(
                          '#${inc['ID'] ?? '-'}',
                          style: TextStyle(
                            color: SupervisorDashboard.warningColor,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    );
                  },
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

class UserShiftUpdateForm extends StatefulWidget {
  final Map<String, dynamic> userData;
  final List<dynamic> shifts;

  const UserShiftUpdateForm({required this.userData, required this.shifts, super.key});

  @override
  State<UserShiftUpdateForm> createState() => _UserShiftUpdateFormState();
}

class _UserShiftUpdateFormState extends State<UserShiftUpdateForm> {
  late int selectedShiftId;

  @override
  void initState() {
    super.initState();
    selectedShiftId = widget.userData['IDTurno'];
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 16, horizontal: 8),
      elevation: 3,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextFormField(
              initialValue: widget.userData['Nombre'],
              decoration: InputDecoration(labelText: 'Nombre'),
              readOnly: true,
              enabled: false,
            ),
            TextFormField(
              initialValue: widget.userData['Apellido'],
              decoration: InputDecoration(labelText: 'Apellido'),
              readOnly: true,
              enabled: false,
            ),
            TextFormField(
              initialValue: widget.userData['Correo'],
              decoration: InputDecoration(labelText: 'Correo'),
              readOnly: true,
              enabled: false,
            ),
            // Puedes agregar más campos bloqueados si lo deseas
            DropdownButtonFormField<int>(
              value: selectedShiftId,
              decoration: InputDecoration(labelText: 'Turno'),
              items: widget.shifts
                  .map<DropdownMenuItem<int>>(
                    (s) => DropdownMenuItem<int>(
                      value: s['ID'],
                      child: Text(s['TipoTurno'] ?? 'Turno'),
                    ),
                  )
                  .toList(),
              onChanged: (val) {
                setState(() {
                  selectedShiftId = val!;
                });
              },
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () async {
                // Solo permite modificar el turno, los demás campos se envían igual que están
                final response = await http.post(
                  Uri.parse('${AppConfig.baseUrl}/user/update'),
                  body: {
                    "ID": widget.userData['ID'].toString(),
                    "Identificacion": widget.userData['Identificacion'].toString(),
                    "Nombre": widget.userData['Nombre'],
                    "Apellido": widget.userData['Apellido'],
                    "Correo": widget.userData['Correo'],
                    "Contrasena": widget.userData['Contrasena'],
                    "IDRolUsuario": widget.userData['IDRolUsuario'].toString(),
                    "IDTurno": selectedShiftId.toString(),
                    "IDTarjeta": widget.userData['IDTarjeta'].toString(),
                  },
                );
                if (response.statusCode == 200) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('Turno actualizado')),
                  );
                } else {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('Error al actualizar turno')),
                  );
                }
              },
              child: Text('Actualizar Turno'),
            ),
          ],
        ),
      ),
    );
  }
}