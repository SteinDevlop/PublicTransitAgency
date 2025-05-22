import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../config/config.dart';
import 'package:flutter/services.dart';

class AdministradorPanel extends StatefulWidget {
  final String token;

  const AdministradorPanel({Key? key, required this.token}) : super(key: key);

  @override
  State<AdministradorPanel> createState() => _AdministradorPanelState();
}

class _AdministradorPanelState extends State<AdministradorPanel> {
  String selectedSection = 'dashboard';
  Map<String, bool> crudOpen = {
    'rutas': false,
    'usuarios': false,
    'operarios': false,
    'mantenimiento': false,
    'supervisores': false,
    'horario': false,
    'tarifa': false,
    'otros': false,
  };

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
    // Colores
    const primaryColor = Color(0xFF1A73E8);
    const secondaryColor = Color(0xFF34A853);
    const accentColor = Color(0xFFFBBC05);
    const cardColor = Color(0xFFF8F9FA);

    return Scaffold(
      appBar: AppBar(
        elevation: 0,
        backgroundColor: primaryColor,
        title: const Text(
          'Panel del Administrador',
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
            width: 270,
            color: const Color(0xFFF8F9FA),
            child: ListView(
              padding: const EdgeInsets.symmetric(vertical: 0, horizontal: 0),
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(
                      vertical: 24, horizontal: 16),
                  color: primaryColor.withOpacity(0.05),
                  child: Row(
                    children: [
                      CircleAvatar(
                        backgroundColor: accentColor,
                        radius: 24,
                        child: const Icon(Icons.admin_panel_settings, color: Colors.white),
                      ),
                      const SizedBox(width: 12),
                      const Expanded(
                        child: Text(
                          'Administrador',
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 16,
                            color: Color(0xFF202124),
                          ),
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                    ],
                  ),
                ),
                const Divider(height: 1),
                _buildMenuButton(
                  icon: Icons.directions_bus,
                  label: 'Actualizar Flota',
                  isActive: selectedSection == 'flota',
                  onTap: () => setState(() => selectedSection = 'flota'),
                ),
                _buildMenuButton(
                  icon: Icons.build_circle_outlined,
                  label: 'Agendar Mantenimiento',
                  isActive: selectedSection == 'mantenimiento',
                  onTap: () => setState(() => selectedSection = 'mantenimiento'),
                ),
                _buildMenuButton(
                  icon: Icons.alt_route,
                  label: 'Asignar Ruta Vehículo',
                  isActive: selectedSection == 'asignar_ruta',
                  onTap: () => setState(() => selectedSection = 'asignar_ruta'),
                ),
                _buildMenuButton(
                  icon: Icons.person_add_alt_1,
                  label: 'Crear Usuario',
                  isActive: selectedSection == 'crear_usuario',
                  onTap: () => setState(() => selectedSection = 'crear_usuario'),
                ),
                _buildMenuButton(
                  icon: Icons.question_answer,
                  label: 'Gestion de PQR',
                  isActive: selectedSection == 'pqr',
                  onTap: () => setState(() => selectedSection = 'pqr'),
                ),
                _buildMenuButton(
                  icon: Icons.bar_chart,
                  label: 'Gestion de Rendimiento',
                  isActive: selectedSection == 'rendimiento',
                  onTap: () => setState(() => selectedSection = 'rendimiento'),
                ),
                _buildMenuButton(
                  icon: Icons.check_circle_outline,
                  label: 'Gestion de Asistencia',
                  isActive: selectedSection == 'asistencia',
                  onTap: () => setState(() => selectedSection = 'asistencia'),
                ),
                const Padding(
                  padding: EdgeInsets.only(left: 16, top: 16, bottom: 8),
                  child: Text(
                    'Gestión CRUD',
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      color: Color(0xFF5F6368),
                      fontSize: 13,
                    ),
                  ),
                ),
                _buildCrudSection('Rutas', 'rutas', [
                  _buildCrudOption('➕ Añadir Ruta', () {}),
                  _buildCrudOption('📄 Leer Rutas', () {}),
                  _buildCrudOption('🖊️ Actualizar Ruta', () {}),
                  _buildCrudOption('🗑️ Eliminar Ruta', () {}),
                ]),
                _buildCrudSection('Usuarios', 'usuarios', [
                  _buildCrudOption('📄 Leer Usuarios', () {}),
                  _buildCrudOption('🖊️ Actualizar Usuario', () {}),
                  _buildCrudOption('🗑️ Eliminar Usuario', () {}),
                ]),
                _buildCrudSection('Operarios', 'operarios', [
                  _buildCrudOption('📄 Leer Operarios', () {}),
                  _buildCrudOption('🖊️ Actualizar Operarios', () {}),
                  _buildCrudOption('🗑️ Eliminar Operarios', () {}),
                ]),
                _buildCrudSection('Mantenimiento', 'mantenimiento', [
                  _buildCrudOption('➕ Añadir Mantenimiento', () {}),
                  _buildCrudOption('📄 Leer Mantenimientos', () {}),
                  _buildCrudOption('🖊️ Actualizar Mantenimiento', () {}),
                  _buildCrudOption('🗑️ Eliminar Mantenimiento', () {}),
                ]),
                _buildCrudSection('Supervisores', 'supervisores', [
                  _buildCrudOption('📄 Leer Supervisores', () {}),
                  _buildCrudOption('🖊️ Actualizar Supervisores', () {}),
                  _buildCrudOption('🗑️ Eliminar Supervisores', () {}),
                ]),
                _buildCrudSection('Horario', 'horario', [
                  _buildCrudOption('➕ Añadir horario', () {}),
                  _buildCrudOption('📄 Leer horario', () {}),
                  _buildCrudOption('🖊️ Actualizar horario', () {}),
                  _buildCrudOption('🗑️ Eliminar horario', () {}),
                ]),
                _buildCrudSection('Tarifa', 'tarifa', [
                  _buildCrudOption('➕ Añadir Tarifa', () {}),
                  _buildCrudOption('📄 Leer Tarifa', () {}),
                  _buildCrudOption('🖊️ Actualizar Tarifa', () {}),
                  _buildCrudOption('🗑️ Eliminar Tarifa', () {}),
                ]),
                _buildCrudSection('Otros', 'otros', [
                  _buildCrudOption('📄 Extraer Tipo de Usuario', () {}),
                  _buildCrudOption('📄 Extraer Tipo de Movimiento', () {}),
                  _buildCrudOption('📄 Extraer Servicios de Transporte', () {}),
                ]),
              ],
            ),
          ),
          // Main content
          Expanded(
            child: Container(
              color: const Color(0xFFF5F7FA),
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(24),
                child: selectedSection == 'dashboard'
                    ? _buildDashboard(primaryColor, cardColor)
                    : _buildSectionContent(selectedSection),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMenuButton({
    required IconData icon,
    required String label,
    required bool isActive,
    required VoidCallback onTap,
  }) {
    return ListTile(
      leading: Icon(icon, color: isActive ? Color(0xFF1A73E8) : Color(0xFF5F6368)),
      title: Text(
        label,
        style: TextStyle(
          fontSize: 14,
          fontWeight: isActive ? FontWeight.w600 : FontWeight.w500,
          color: isActive ? Color(0xFF1A73E8) : Color(0xFF202124),
        ),
      ),
      dense: true,
      horizontalTitleGap: 8,
      onTap: onTap,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8),
      ),
      tileColor: isActive ? Color(0xFF1A73E8).withOpacity(0.1) : null,
      hoverColor: Color(0xFF1A73E8).withOpacity(0.05),
    );
  }

  Widget _buildCrudSection(String title, String key, List<Widget> options) {
    final isOpen = crudOpen[key] ?? false;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        ListTile(
          leading: Icon(
            isOpen ? Icons.expand_more : Icons.chevron_right,
            color: Color(0xFF5F6368),
          ),
          title: Text(
            title,
            style: const TextStyle(
              fontWeight: FontWeight.w600,
              fontSize: 14,
              color: Color(0xFF5F6368),
            ),
          ),
          onTap: () {
            setState(() {
              crudOpen[key] = !isOpen;
            });
          },
        ),
        if (isOpen)
          Padding(
            padding: const EdgeInsets.only(left: 32),
            child: Column(children: options),
          ),
      ],
    );
  }

  Widget _buildCrudOption(String label, VoidCallback onTap) {
    return ListTile(
      title: Text(label, style: const TextStyle(fontSize: 13)),
      dense: true,
      onTap: onTap,
      contentPadding: const EdgeInsets.symmetric(horizontal: 8),
    );
  }

  Widget _buildDashboard(Color primaryColor, Color cardColor) {
    return FutureBuilder<Map<String, dynamic>>(
      future: fetchDashboardData(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return _loadingWidget('Cargando información...');
        } else if (snapshot.hasError) {
          return _errorWidget('Error al cargar información');
        } else if (!snapshot.hasData) {
          return _emptyWidget('Sin datos disponibles');
        }
        final data = snapshot.data!;
        final totalVehiculos = data['total_vehiculos']?.toString() ?? '0';
        final totalPasajeros = data['total_passanger']?.toString() ?? '0';
        final totalOperarios = data['total_operative']?.toString() ?? '0';
        final totalSupervisores = data['total_supervisors']?.toString() ?? '0';

        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Panel General del Administrador',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Color(0xFF202124),
              ),
            ),
            const SizedBox(height: 24),
            Row(
              children: [
                _buildDashboardCard('Total de Vehículos', totalVehiculos, primaryColor, cardColor),
                const SizedBox(width: 16),
                _buildDashboardCard('Usuarios Registrados', totalPasajeros, primaryColor, cardColor),
                const SizedBox(width: 16),
                _buildDashboardCard('Operarios Activos', totalOperarios, primaryColor, cardColor),
                const SizedBox(width: 16),
                _buildDashboardCard('Supervisores', totalSupervisores, primaryColor, cardColor),
              ],
            ),
          ],
        );
      },
    );
  }

  Widget _buildDashboardCard(String title, String value, Color color, Color cardColor) {
    return Expanded(
      child: Card(
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
          side: BorderSide(
            color: color.withOpacity(0.1),
            width: 1,
          ),
        ),
        color: cardColor,
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w500,
                  color: color,
                ),
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
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSectionContent(String section) {
    // Aquí puedes agregar el contenido de cada sección si lo deseas.
    return Center(
      child: Text(
        'Sección: $section\n(Pendiente de implementar)',
        style: const TextStyle(fontSize: 18, color: Color(0xFF5F6368)),
        textAlign: TextAlign.center,
      ),
    );
  }

  Widget _loadingWidget(String text) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const CircularProgressIndicator(
            color: Color(0xFF1A73E8),
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
}