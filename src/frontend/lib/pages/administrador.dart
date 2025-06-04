import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter/services.dart';
import '../config/config.dart';

class AdminPanel extends StatelessWidget {
  final String token;

  const AdminPanel({Key? key, required this.token}) : super(key: key);

  // Define our color scheme
  static const primaryColor = Color(0xFF1A73E8); // Blue
  static const secondaryColor = Color(0xFF34A853); // Green accent
  static const accentColor = Color(0xFFFBBC05); // Yellow accent
  static const warningColor = Color(0xFFEA4335); // Red for alerts
  static const backgroundColor = Colors.white;
  static const cardColor = Color(0xFFF8F9FA); // Light gray/white

  Future<Map<String, dynamic>> fetchDashboardData() async {
    print('Token enviado: $token');
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/login/dashboard'),
      headers: {
        'Authorization': 'Bearer $token',
        'accept': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      final dashboardData = json.decode(response.body);
      print('Datos del dashboard: $dashboardData');
      return dashboardData;
    } else {
      print('Error al obtener el dashboard: ${response.body}');
      throw Exception('Error al cargar datos del dashboard: ${response.body}');
    }
  }

    Future<List<dynamic>> fetchTransportUnits() async {
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/transport_units/with_names'),
      headers: {
        'Authorization': 'Bearer $token',
        'accept': 'application/json',
      },
    );
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Error al cargar unidades de transporte');
    }
  }
  Future<bool> createTransportUnit(Map<String, dynamic> data) async {
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/transport_units/create'),
      headers: {
        'Authorization': 'Bearer $token',
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: data,
    );
    return response.statusCode == 200 || response.statusCode == 201;
  }

  Future<bool> updateTransportUnit(Map<String, dynamic> data) async {
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/transport_units/update'),
      headers: {
        'Authorization': 'Bearer $token',
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: data,
    );
    return response.statusCode == 200;
  }

  Future<bool> deleteTransportUnit(String id) async {
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/transport_units/delete'),
      headers: {
        'Authorization': 'Bearer $token',
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: {'ID': id},
    );
    return response.statusCode == 200;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        elevation: 0,
        backgroundColor: primaryColor,
        title: const Text(
          'Panel de Administración',
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
      body: FutureBuilder<Map<String, dynamic>>(
        future: fetchDashboardData(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  CircularProgressIndicator(
                    color: primaryColor,
                    strokeWidth: 3,
                  ),
                  const SizedBox(height: 16),
                  const Text(
                    'Cargando información del sistema...',
                    style: TextStyle(
                      color: Color(0xFF5F6368),
                      fontSize: 16,
                    ),
                  ),
                ],
              ),
            );
          } else if (snapshot.hasError) {
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
                    'Error: ${snapshot.error}',
                    style: const TextStyle(color: Colors.red),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            );
          } else if (!snapshot.hasData) {
            return const Center(
              child: Text(
                'Sin datos disponibles',
                style: TextStyle(fontSize: 18),
              ),
            );
          }

          final data = snapshot.data!;
          final user = data['user'] ?? {};
          final totalVehiculos = data['total_vehiculos'] ?? 0;
          final totalPasajeros = data['total_passanger'] ?? 0;
          final totalOperarios = data['total_operative'] ?? 0;
          final totalSupervisores = data['total_supervisors'] ?? 0;

          return Row(
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
                      color: primaryColor.withOpacity(0.05),
                      child: Row(
                        children: [
                          CircleAvatar(
                            backgroundColor: primaryColor,
                            radius: 24,
                            child: Text(
                              user['Nombre']?.toString().substring(0, 1) ?? 'A',
                              style: const TextStyle(
                                color: Colors.white,
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
                                Text(
                                  user['Nombre']?.toString() ?? 'Administrador',
                                  style: const TextStyle(
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
                                    color: primaryColor,
                                    borderRadius: BorderRadius.circular(12),
                                  ),
                                  child: const Text(
                                    'Administrador',
                                    style: TextStyle(
                                      color: Colors.white,
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
                            color: primaryColor,
                            isActive: true,
                          ),
                          _buildMenuItem(
  icon: Icons.alt_route,
  title: 'Gestión Ruta-Parada',
  color: primaryColor,
  onTap: () {
    showDialog(
      context: context,
      builder: (_) => Dialog(
        child: SizedBox(
          width: 500,
          child: RutaParadaCrudWidget(token: token),
        ),
      ),
    );
  },
),
_buildMenuItem(
  icon: Icons.directions_bus,
  title: 'Actualizar Flota',
  color: primaryColor,
  onTap: () async {
    final unidades = await fetchTransportUnits();
    showDialog(
      context: context,
      builder: (_) => Dialog(
        child: SizedBox(
          width: 400,
          child: ListView.builder(
            shrinkWrap: true,
            itemCount: unidades.length,
            itemBuilder: (context, i) {
              final unidad = unidades[i];
              return ListTile(
                title: Text('Unidad #${unidad['ID']}'),
                subtitle: Text('Ubicación: ${unidad['Ubicacion']}'),
                trailing: Icon(Icons.edit),
                onTap: () {
                  Navigator.pop(context);
                  showDialog(
                    context: context,
                    builder: (_) => Dialog(
                      child: EditarUnidadWidget(
                        token: token,
                        unidad: unidad,
                        onUpdated: () => (context as Element).markNeedsBuild(),
                      ),
                    ),
                  );
                },
              );
            },
          ),
        ),
      ),
    );
  },

                          ),
                          _buildMenuItem(
                            icon: Icons.build_circle_outlined,
                            title: 'Agendar Mantenimiento',
                            color: primaryColor,
                            onTap: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (_) =>
                                      AgendarMantenimientoScreen(token: token),
                                ),
                              );
                            },
                          ),
_buildMenuItem(
  icon: Icons.alt_route,
  title: 'Asignar Ruta Vehículo',
  color: primaryColor,
  onTap: () async {
    final unidades = await fetchTransportUnits();
    showDialog(
      context: context,
      builder: (_) => Dialog(
        child: SizedBox(
          width: 400,
          child: ListView.builder(
            shrinkWrap: true,
            itemCount: unidades.length,
            itemBuilder: (context, i) {
              final unidad = unidades[i];
              return ListTile(
                title: Text('Unidad #${unidad['ID']}'),
                subtitle: Text('Ruta actual: ${unidad['NombreRuta'] ?? '-'}'),
                trailing: Icon(Icons.alt_route),
                onTap: () {
                  Navigator.pop(context);
                  showDialog(
                    context: context,
                    builder: (_) => Dialog(
                      child: AsignarRutaUnidadWidget(
                        token: token,
                        unidad: unidad,
                        onUpdated: () => (context as Element).markNeedsBuild(),
                      ),
                    ),
                  );
                },
              );
            },
          ),
        ),
      ),
    );
  },
),
                          _buildMenuItem(
                            icon: Icons.person_add_alt_1,
                            title: 'Crear Usuario',
                            color: primaryColor,
                            onTap: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (_) =>
                                      CrearUsuarioScreen(token: token),
                                ),
                              );
                            },
                          ),
                          _buildMenuItem(
                            icon: Icons.question_answer_outlined,
                            title: 'Gestión de PQR',
                            color: primaryColor,
                            onTap: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (_) =>
                                      PqrCrudWidget(
                                        token: token,
                                        onBack: () => Navigator.of(context).pop(),
                                        onSuccess: () => Navigator.pop(context)),
                                ),
                              );
                            },
                          ),
                          _buildMenuItem(
                            icon: Icons.bar_chart_outlined,
                            title: 'Gestión de Rendimiento',
                            color: primaryColor,
                            onTap: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (_) =>
                                      BehaviorCrudWidget(
                                        token: token,
                                        onBack: () => Navigator.of(context).pop(),
                                        onSuccess: () => Navigator.pop(context)),
                                ),
                              );
                            },
                          ),
                          _buildMenuItem(
                            icon: Icons.assignment_turned_in_outlined,
                            title: 'Gestión de Asistencia',
                            color: primaryColor,
                            onTap: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (_) =>
                                      AsistanceCrudWidget(
                                        token: token,
                                        onBack: () => Navigator.of(context).pop(),
                                        onSuccess: () => Navigator.pop(context)),
                                ),
                              );
                            },
                          ),
                          // CRUD: Rutas
                          _buildCrudSection(
                            title: 'Rutas',
                            color: primaryColor,
                            buttons: [
                              _buildCrudButton(
                                '➕ Añadir Ruta',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: _RutaFormWidget(
                                        token: token,
                                        mode: RutaFormMode.create,
                                        onSuccess: () => Navigator.pop(context),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              _buildCrudButton(
                                '📄 Leer Rutas',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: _RutaListWidget(token: token),
                                    ),
                                  ),
                                ),
                              ),
                              _buildCrudButton(
                                '🖊️ Actualizar Ruta',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: _RutaFormWidget(
                                        token: token,
                                        mode: RutaFormMode.update,
                                        onSuccess: () => Navigator.pop(context),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              _buildCrudButton(
                                '🗑️ Eliminar Ruta',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: _RutaDeleteWidget(
                                        token: token,
                                        onSuccess: () => Navigator.pop(context),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                            ],
                          ),
                          // CRUD: Usuario
                          _buildCrudSection(
                            title: 'Usuarios',
                            color: primaryColor,
                            buttons: [
                              _buildCrudButton(
                                  '📄 Buscar Usuario',
                                  () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: ConsultarUsuarioScreen(
                                        token: token,
                                        onSuccess: () => Navigator.pop(context),
                                      ),
                                    ),
                                  ),
                                ),),
                              _buildCrudButton(
                                  '🖊️ Actualizar Usuario',
                                  () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: ActualizarUsuarioScreen(
                                        token: token,
                                        mode: ActualizarUsuarioFormMode.update,
                                        onSuccess: () => Navigator.pop(context),
                                      ),
                                    ),
                                  ),
                                ),),
                              _buildCrudButton(
                                  '🗑️ Eliminar Usuario',
                                  () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: EliminarUsuarioScreen(
                                        token: token,
                                        mode: EliminarUsuarioFormMode.normal,
                                        onSuccess: () => Navigator.pop(context),
                                      ),
                                    ),
                                  ),
                                ),),
                            ],
                          ),
                          // CRUD: Mantenimiento
                          _buildCrudSection(
                            title: 'Mantenimiento',
                            color: primaryColor,
                            buttons: [
                              _buildCrudButton(
                                '➕ Añadir Mantenimiento',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                      child: AgendarMantenimientoScreen(
                                          token: token)),
                                ),
                              ),
                              _buildCrudButton(
                                '📄 Leer Mantenimientos',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                      child: LeerMantenimientosWidget(
                                          token: token)),
                                ),
                              ),
                              _buildCrudButton(
                                '🖊️ Actualizar Mantenimiento',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                      child: ActualizarMantenimientoWidget(
                                          token: token)),
                                ),
                              ),
                              _buildCrudButton(
                                '🗑️ Eliminar Mantenimiento',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                      child: EliminarMantenimientoWidget(
                                          token: token)),
                                ),
                              ),
                            ],
                          ),
                          // CRUD: Horario
                          _buildCrudSection(
                            title: 'Horario',
                            color: primaryColor,
                            buttons: [
                              _buildCrudButton(
                                '➕ Añadir horario',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: _HorarioFormWidget(
                                        token: token,
                                        mode: HorarioFormMode.create,
                                        onSuccess: () => Navigator.pop(context),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              _buildCrudButton(
                                '📄 Leer horario',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: _HorarioListWidget(token: token),
                                    ),
                                  ),
                                ),
                              ),
                              _buildCrudButton(
                                '🖊️ Actualizar horario',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: _HorarioFormWidget(
                                        token: token,
                                        mode: HorarioFormMode.update,
                                        onSuccess: () => Navigator.pop(context),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              _buildCrudButton(
                                '🗑️ Eliminar horario',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: _HorarioDeleteWidget(
                                        token: token,
                                        onSuccess: () => Navigator.pop(context),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                            ],
                          ),
                          // CRUD: Tarifa
                          _buildCrudSection(
                            title: 'Tarifa',
                            color: primaryColor,
                            buttons: [
                            _buildCrudButton(
                                '➕ Añadir Tarifa',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: CreatePriceWidget(
                                        token: token,
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              _buildCrudButton(
                                '📄 Leer Tarifa',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: SizedBox(
                                        width: 360,
                                        child: AdminPricesListWidget(
                                          token: token,
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              _buildCrudButton(
                                  '🖊️ Actualizar Tarifa',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: UpdatePriceFlow(
                                        token: token,
                                        onCancel: () => Navigator.of(context).pop(),
                                        onSuccess: () => Navigator.pop(context)),
                                      ),
                                    ),
                                  ),
                                ),
                              _buildCrudButton(
                                  '🗑️ Eliminar Tarifa',
                                  () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: DeletePriceWidget(
                                        token: token,
                                        onCancel: () => Navigator.of(context).pop(),
                                        onSuccess: () => Navigator.pop(context)),
                                      ),
                                    ),
                                  ),),
                            ],
                          ),
                          // CRUD: Otros
                          _buildCrudSection(
                            title: 'Otros',
                            color: primaryColor,
                            buttons: [
                              _buildCrudButton(
                                  '📄 Gestión de Tipo de Usuario',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: RolUserCrudTabsWidget(
                                        token: token,
                                        onSuccess: () => Navigator.pop(context),
                                      ),
                                    ),
                                  ),
                                ),),
                              _buildCrudButton(
                                  '📄 Gestión de Tipo de Movimiento',
                                  () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: TypeMovementCrudTabsWidget(
                                        token: token,
                                        onSuccess: () => Navigator.pop(context),
                                      ),
                                    ),
                                  ),
                                  ),
                              ),
                              _buildCrudButton(
                                  '📄 Gestion de Servicios de Transporte',
                                  () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: TypeTransportCrudTabsWidget(
                                        token: token,
                                        onSuccess: () => Navigator.pop(context),
                                      ),
                                    ),
                                  ),
                                  ),),
                            ],
                          ),
                        ],
                      ),
                    ),

                    // Logout Button
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(16),
                      child: ElevatedButton.icon(
                        onPressed: () {},
                        icon: const Icon(Icons.logout, size: 18),
                        label: const Text('Cerrar Sesión'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.white,
                          foregroundColor: primaryColor,
                          elevation: 0,
                          padding: const EdgeInsets.symmetric(vertical: 12),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(8),
                            side: BorderSide(color: primaryColor),
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
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Header with date and welcome message
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  children: [
                                    const Icon(
                                      Icons.dashboard_outlined,
                                      color: primaryColor,
                                      size: 28,
                                    ),
                                    const SizedBox(width: 12),
                                    const Text(
                                      'Panel de Control',
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
                                  'Bienvenido, ${user['Nombre'] ?? 'Administrador'}. Aquí está el resumen del sistema.',
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
                                    color: primaryColor,
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

                        // Stats Overview
                        Row(
                          children: [
                            Expanded(
                              child: _buildStatCard(
                                title: 'Total Vehículos',
                                value: '$totalVehiculos',
                                icon: Icons.directions_bus,
                                color: primaryColor,
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: _buildStatCard(
                                title: 'Total Pasajeros',
                                value: '$totalPasajeros',
                                icon: Icons.people,
                                color: secondaryColor,
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: _buildStatCard(
                                title: 'Total Operarios',
                                value: '$totalOperarios',
                                icon: Icons.engineering,
                                color: accentColor,
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: _buildStatCard(
                                title: 'Total Supervisores',
                                value: '$totalSupervisores',
                                icon: Icons.supervisor_account,
                                color: warningColor,
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 24),

                        // Quick Actions
                        Card(
                          elevation: 0,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(12),
                            side: BorderSide(
                              color: primaryColor.withOpacity(0.1),
                              width: 1,
                            ),
                          ),
                          color: cardColor,
                          child: Padding(
                            padding: const EdgeInsets.all(20),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  children: [
                                    Icon(
                                      Icons.flash_on,
                                      color: primaryColor,
                                      size: 22,
                                    ),
                                    const SizedBox(width: 8),
                                    const Text(
                                      'Acciones Rápidas',
                                      style: TextStyle(
                                        fontSize: 18,
                                        fontWeight: FontWeight.bold,
                                        color: Color(0xFF202124),
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 16),
                                const Divider(),
                                const SizedBox(height: 16),
                                GridView.count(
                                  shrinkWrap: true,
                                  physics: const NeverScrollableScrollPhysics(),
                                  crossAxisCount: 2,
                                  crossAxisSpacing: 16,
                                  mainAxisSpacing: 16,
                                  childAspectRatio: 2.5,
                                  children: [
                                    _buildActionButton(
                                      label: 'Añadir Usuario',
                                      icon: Icons.person_add_outlined,
                                      color: primaryColor,
                                      onPressed: () => showDialog(
                                        context: context,
                                        builder: (_) => Dialog(
                                          child: CrearUsuarioWidget(
                                            token: token,
                                            onCreated: () =>
                                                Navigator.pop(context),
                                          ),
                                        ),
                                      ),
                                    ),
                                    _buildActionButton(
                                      label: 'Añadir Vehículo',
                                      icon: Icons.add_circle_outline,
                                      color: secondaryColor,
                                      onPressed: () => showDialog(
                                        context: context,
                                        builder: (_) => Dialog(
                                          child: CrearUnidadWidget(
                                            token: token,
                                            onCreated: () =>
                                                Navigator.pop(context),
                                          ),
                                        ),
                                      ),
                                    ),
                                    _buildActionButton(
                                      label: 'Generar Reporte',
                                      icon: Icons.assessment_outlined,
                                      color: accentColor,
                                    ),
                                    _buildActionButton(
                                      label: 'Registrar Asistencia',
                                      icon: Icons.person_add_outlined,
                                      color: const Color.fromARGB(255, 232, 36, 26),
                                      onPressed: () => showDialog(
                                        context: context,
                                        builder: (_) => Dialog(
                                          child: CrearAsistenciaScreen(
                                            token: token,
                                          ),
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(height: 24),

                        // Transport Units Management
                        const SizedBox(height: 32),
                        Text('Gestión de Flota',
                            style: TextStyle(
                                fontSize: 22, fontWeight: FontWeight.bold)),
                        const SizedBox(height: 16),
                        Row(
                          children: [
                            ElevatedButton.icon(
                              icon: Icon(Icons.add),
                              label: Text('Añadir Unidad'),
                              style: ElevatedButton.styleFrom(
                                backgroundColor: AdminPanel.primaryColor,
                                foregroundColor: Colors.white,
                              ),
                              onPressed: () {
                                showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: CrearUnidadWidget(
                                      token: token,
                                      onCreated: () => Navigator.pop(context),
                                    ),
                                  ),
                                );
                              },
                            ),
                            const SizedBox(width: 16),
                            ElevatedButton.icon(
                              icon: Icon(Icons.refresh),
                              label: Text('Actualizar Tabla'),
                              onPressed: () {
                                (context as Element).markNeedsBuild();
                              },
                            ),
                          ],
                        ),
                        const SizedBox(height: 24),
                        _buildTransportUnitsSection(),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          );
        },
      ),
    );
  }

  Widget _buildTransportUnitsSection() {
    return FutureBuilder<List<dynamic>>(
      future: fetchTransportUnits(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return Center(child: CircularProgressIndicator());
        } else if (snapshot.hasError) {
          return Center(
              child: Text('Error al cargar unidades de transporte'));
        } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
          return Center(child: Text('No hay unidades registradas.'));
        }
        final units = snapshot.data!;
return DataTable(
  columns: const [
    DataColumn(label: Text('ID')),
    DataColumn(label: Text('Ubicación')),
    DataColumn(label: Text('Capacidad')),
    DataColumn(label: Text('Ruta')),
    DataColumn(label: Text('Tipo')),
    DataColumn(label: Text('Acciones')),
  ],
  rows: units.map<DataRow>((unit) {
    return DataRow(
      cells: [
        DataCell(Text(unit['ID']?.toString() ?? '-')),
        DataCell(Text(unit['Ubicacion']?.toString() ?? '-')),
        DataCell(Text(unit['Capacidad']?.toString() ?? '-')),
        DataCell(Text(unit['NombreRuta']?.toString() ?? '-')), // Cambiado
        DataCell(Text(unit['NombreTipoTransporte']?.toString() ?? '-')), // Cambiado
        DataCell(Row(
          children: [
            IconButton(
              icon: Icon(Icons.edit, color: Colors.blue),
              tooltip: 'Editar',
              onPressed: () {
                showDialog(
                  context: context,
                  builder: (_) => Dialog(
                    child: EditarUnidadWidget(
                      token: token,
                      unidad: unit,
                      onUpdated: () =>
                          (context as Element).markNeedsBuild(),
                    ),
                  ),
                );
              },
            ),
            IconButton(
              icon: Icon(Icons.delete, color: Colors.red),
              tooltip: 'Eliminar',
              onPressed: () async {
                final confirm = await showDialog<bool>(
                  context: context,
                  builder: (_) => AlertDialog(
                    title: Text('Eliminar unidad'),
                    content: Text(
                        '¿Seguro que deseas eliminar esta unidad?'),
                    actions: [
                      TextButton(
                        onPressed: () =>
                            Navigator.pop(context, false),
                        child: Text('Cancelar'),
                      ),
                      TextButton(
                        onPressed: () =>
                            Navigator.pop(context, true),
                        child: Text('Eliminar'),
                      ),
                    ],
                  ),
                );
                if (confirm == true) {
                  await deleteTransportUnit(unit['ID'].toString());
                  (context as Element).markNeedsBuild();
                }
              },
            ),
          ],
        )),
      ],
    );
  }).toList(),
);
      },
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
      color: cardColor,
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
          ],
        ),
      ),
    );
  }

  Widget _buildActionButton({
    required String label,
    required IconData icon,
    required Color color,
    VoidCallback? onPressed,
  }) {
    return ElevatedButton.icon(
      onPressed: onPressed,
      icon: Icon(icon, size: 18),
      label: Text(label),
      style: ElevatedButton.styleFrom(
        backgroundColor: color,
        foregroundColor: Colors.white,
        padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
        elevation: 0,
        alignment: Alignment.centerLeft,
      ),
    );
  }

  Widget _buildCrudSection(
      {required String title,
      required Color color,
      required List<Widget> buttons}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0, horizontal: 8.0),
      child: Card(
        color: color.withOpacity(0.04),
        elevation: 0,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
        child: ExpansionTile(
          title: Text(title,
              style: TextStyle(fontWeight: FontWeight.bold, color: color)),
          children: buttons,
        ),
      ),
    );
  }

  Widget _buildCrudButton(String label, VoidCallback onPressed) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2.0, horizontal: 16.0),
      child: SizedBox(
        width: double.infinity,
        child: OutlinedButton(
          onPressed: onPressed,
          child: Align(
            alignment: Alignment.centerLeft,
            child: Text(label, style: const TextStyle(fontSize: 14)),
          ),
          style: OutlinedButton.styleFrom(
            padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 12),
            side: const BorderSide(color: Color(0xFFDFE1E5)),
            shape:
                RoundedRectangleBorder(borderRadius: BorderRadius.circular(6)),
          ),
        ),
      ),
    );
  }
}

// Agrego la pantalla para agendar mantenimiento
class AgendarMantenimientoScreen extends StatefulWidget {
  final String token;
  const AgendarMantenimientoScreen({Key? key, required this.token})
      : super(key: key);

  static const primaryColor = Color(0xFF1A73E8);

  @override
  State<AgendarMantenimientoScreen> createState() =>
      _AgendarMantenimientoScreenState();
}

class _AgendarMantenimientoScreenState
    extends State<AgendarMantenimientoScreen> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _idController = TextEditingController();
  final TextEditingController _idStatusController = TextEditingController();
  final TextEditingController _typeController = TextEditingController();
  final TextEditingController _fechaController = TextEditingController();
  final TextEditingController _idUnidadController = TextEditingController();
  bool _loading = false;
  String? _response;
  String? _error;

  Future<void> _agendarMantenimiento() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _response = null;
      _error = null;
    });
    try {
      final response = await http.post(
        Uri.parse('${AppConfig.baseUrl}/maintainance/create'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: {
          'ID': _idController.text.trim(),
          'id_status': _idStatusController.text.trim(),
          'type': _typeController.text.trim(),
          'fecha': _fechaController.text.trim(),
          'idunidad': _idUnidadController.text.trim(),
        },
      );
      if (response.statusCode == 200 || response.statusCode == 201) {
        setState(() {
          _response = 'Mantenimiento agendado exitosamente.';
        });
      } else {
        setState(() {
          _error = 'No se pudo agendar el mantenimiento. (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión.';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Agendar Mantenimiento'),
        backgroundColor: AgendarMantenimientoScreen.primaryColor,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Complete los datos para agendar un mantenimiento:',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 24),
              TextFormField(
                controller: _idController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(
                  labelText: 'ID',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.confirmation_number),
                ),
                validator: (value) =>
                    value == null || value.isEmpty ? 'Ingrese el ID' : null,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _idStatusController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(
                  labelText: 'ID Status',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.info_outline),
                ),
                validator: (value) => value == null || value.isEmpty
                    ? 'Ingrese el ID Status'
                    : null,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _typeController,
                decoration: InputDecoration(
                  labelText: 'Tipo de Mantenimiento',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.build),
                ),
                validator: (value) =>
                    value == null || value.isEmpty ? 'Ingrese el tipo' : null,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _fechaController,
                decoration: InputDecoration(
                  labelText: 'Fecha (YYYY-MM-DD HH:MM:SS)',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.date_range),
                ),
                validator: (value) =>
                    value == null || value.isEmpty ? 'Ingrese la fecha' : null,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _idUnidadController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(
                  labelText: 'ID Unidad',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.directions_bus),
                ),
                validator: (value) => value == null || value.isEmpty
                    ? 'Ingrese el ID Unidad'
                    : null,
              ),
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _loading ? null : _agendarMantenimiento,
                  child: _loading
                      ? SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(
                              strokeWidth: 2, color: Colors.white),
                        )
                      : Text('Agendar Mantenimiento'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AgendarMantenimientoScreen.primaryColor,
                    foregroundColor: Colors.white,
                    padding: EdgeInsets.symmetric(vertical: 14),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                ),
              ),
              if (_response != null) ...[
                const SizedBox(height: 24),
                Card(
                  color: Colors.green[50],
                  elevation: 0,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Row(
                      children: [
                        Icon(Icons.check_circle, color: Colors.green[700]),
                        const SizedBox(width: 12),
                        Expanded(
                            child: Text(_response!,
                                style: TextStyle(
                                    color: Colors.green[900],
                                    fontWeight: FontWeight.bold))),
                      ],
                    ),
                  ),
                ),
              ],
              if (_error != null) ...[
                const SizedBox(height: 24),
                Card(
                  color: Colors.red[50],
                  elevation: 0,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Row(
                      children: [
                        Icon(Icons.error, color: Colors.red[700]),
                        const SizedBox(width: 12),
                        Expanded(
                            child: Text(_error!,
                                style: TextStyle(
                                    color: Colors.red[900],
                                    fontWeight: FontWeight.bold))),
                      ],
                    ),
                  ),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}

// Nueva pantalla para leer mantenimientos
class LeerMantenimientosWidget extends StatefulWidget {
  final String token;
  const LeerMantenimientosWidget({Key? key, required this.token})
      : super(key: key);
  @override
  State<LeerMantenimientosWidget> createState() =>
      _LeerMantenimientosWidgetState();
}

class _LeerMantenimientosWidgetState extends State<LeerMantenimientosWidget> {
  bool _loading = true;
  String? _error;
  List<dynamic> _mantenimientos = [];
  @override
  void initState() {
    super.initState();
    _fetch();
  }

  Future<void> _fetch() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/maintainance/listar'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json'
        },
      );
      if (response.statusCode == 200) {
        setState(() {
          _mantenimientos = json.decode(response.body);
        });
      } else {
        setState(() {
          _error = 'No se pudo obtener la lista.';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión.';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 500,
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: _loading
            ? Center(child: CircularProgressIndicator())
            : _error != null
                ? Center(
                    child: Text(_error!, style: TextStyle(color: Colors.red)))
                : _mantenimientos.isEmpty
                    ? const Center(child: Text('No hay mantenimientos.'))
                    : ListView.separated(
                        shrinkWrap: true,
                        itemCount: _mantenimientos.length,
                        separatorBuilder: (_, __) => Divider(),
                        itemBuilder: (_, i) {
                          final m = _mantenimientos[i];
                          return ListTile(
                            title:
                                Text('ID: \\${m['ID']} - Tipo: \\${m['type']}'),
                            subtitle: Text(
                                'Fecha: \\${m['fecha']} | Unidad: \\${m['idunidad']} | Estado: \\${m['id_status']}'),
                          );
                        },
                      ),
      ),
    );
  }
}

// Nueva pantalla para actualizar mantenimiento
class ActualizarMantenimientoWidget extends StatefulWidget {
  final String token;
  const ActualizarMantenimientoWidget({Key? key, required this.token})
      : super(key: key);
  @override
  State<ActualizarMantenimientoWidget> createState() =>
      _ActualizarMantenimientoWidgetState();
}

class _ActualizarMantenimientoWidgetState
    extends State<ActualizarMantenimientoWidget> {
  final _formKey = GlobalKey<FormState>();
  final _idController = TextEditingController();
  final _idStatusController = TextEditingController();
  final _typeController = TextEditingController();
  final _fechaController = TextEditingController();
  final _idUnidadController = TextEditingController();
  bool _loading = false;
  String? _response;
  String? _error;
  Future<void> _actualizar() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _response = null;
      _error = null;
    });
    try {
      final response = await http.post(
        Uri.parse('${AppConfig.baseUrl}/maintainance/update'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: {
          'ID': _idController.text.trim(),
          'id_status': _idStatusController.text.trim(),
          'type': _typeController.text.trim(),
          'fecha': _fechaController.text.trim(),
          'idunidad': _idUnidadController.text.trim(),
        },
      );
      if (response.statusCode == 200) {
        setState(() {
          _response = 'Mantenimiento actualizado exitosamente.';
        });
      } else {
        setState(() {
          _error = 'No se pudo actualizar. (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión.';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 400,
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('Actualizar Mantenimiento',
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
              const SizedBox(height: 16),
              TextFormField(
                controller: _idController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(labelText: 'ID'),
                validator: (v) =>
                    v == null || v.isEmpty ? 'Ingrese el ID' : null,
              ),
              const SizedBox(height: 8),
              TextFormField(
                controller: _idStatusController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(labelText: 'ID Status'),
                validator: (v) =>
                    v == null || v.isEmpty ? 'Ingrese el ID Status' : null,
              ),
              const SizedBox(height: 8),
              TextFormField(
                controller: _typeController,
                decoration: InputDecoration(labelText: 'Tipo de Mantenimiento'),
                validator: (v) =>
                    v == null || v.isEmpty ? 'Ingrese el tipo' : null,
              ),
              const SizedBox(height: 8),
              TextFormField(
                controller: _fechaController,
                decoration:
                    InputDecoration(labelText: 'Fecha (YYYY-MM-DD HH:MM:SS)'),
                validator: (v) =>
                    v == null || v.isEmpty ? 'Ingrese la fecha' : null,
              ),
              const SizedBox(height: 8),
              TextFormField(
                controller: _idUnidadController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(labelText: 'ID Unidad'),
                validator: (v) =>
                    v == null || v.isEmpty ? 'Ingrese el ID Unidad' : null,
              ),
              const SizedBox(height: 16),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _loading ? null : _actualizar,
                  child: _loading
                      ? SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(
                              strokeWidth: 2, color: Colors.white))
                      : Text('Actualizar'),
                ),
              ),
              if (_response != null) ...[
                const SizedBox(height: 16),
                Text(_response!, style: TextStyle(color: Colors.green)),
              ],
              if (_error != null) ...[
                const SizedBox(height: 16),
                Text(_error!, style: TextStyle(color: Colors.red)),
              ],
            ],
          ),
        ),
      ),
    );
  }
}

// Nueva pantalla para eliminar mantenimiento
class EliminarMantenimientoWidget extends StatefulWidget {
  final String token;
  const EliminarMantenimientoWidget({Key? key, required this.token})
      : super(key: key);
  @override
  State<EliminarMantenimientoWidget> createState() =>
      _EliminarMantenimientoWidgetState();
}

class _EliminarMantenimientoWidgetState
    extends State<EliminarMantenimientoWidget> {
  final _formKey = GlobalKey<FormState>();
  final _idController = TextEditingController();
  bool _loading = false;
  String? _response;
  String? _error;
  Future<void> _eliminar() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _response = null;
      _error = null;
    });
    try {
      final response = await http.post(
        Uri.parse('${AppConfig.baseUrl}/maintainance/delete'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: {'ID': _idController.text.trim()},
      );
      if (response.statusCode == 200) {
        setState(() {
          _response = 'Mantenimiento eliminado exitosamente.';
        });
      } else {
        setState(() {
          _error = 'No se pudo eliminar. (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión.';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 350,
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('Eliminar Mantenimiento',
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
              const SizedBox(height: 16),
              TextFormField(
                controller: _idController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(labelText: 'ID'),
                validator: (v) =>
                    v == null || v.isEmpty ? 'Ingrese el ID' : null,
              ),
              const SizedBox(height: 16),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _loading ? null : _eliminar,
                  child: _loading
                      ? SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(
                              strokeWidth: 2, color: Colors.white))
                      : Text('Eliminar'),
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
                ),
              ),
              if (_response != null) ...[
                const SizedBox(height: 16),
                Text(_response!, style: TextStyle(color: Colors.green)),
              ],
              if (_error != null) ...[
                const SizedBox(height: 16),
                Text(_error!, style: TextStyle(color: Colors.red)),
              ],
            ],
          ),
        ),
      ),
    );
  }
}

// Widget para crear unidad de transporte
class CrearUnidadWidget extends StatefulWidget {
  final String token;
  final VoidCallback onCreated;
  const CrearUnidadWidget({required this.token, required this.onCreated, Key? key}) : super(key: key);

  @override
  State<CrearUnidadWidget> createState() => _CrearUnidadWidgetState();
}

class _CrearUnidadWidgetState extends State<CrearUnidadWidget> {
  final _formKey = GlobalKey<FormState>();
  final _idController = TextEditingController(); // <-- Nuevo controlador para ID
  final _ubicacionController = TextEditingController();
  final _capacidadController = TextEditingController();
  final _rutaController = TextEditingController();
  final _tipoController = TextEditingController();
  bool _loading = false;
  String? _error;

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _loading = true);
    final data = {
      'ID': _idController.text.trim(), // <-- Incluye el ID manual
      'Ubicacion': _ubicacionController.text.trim(),
      'Capacidad': _capacidadController.text.trim(),
      'IDRuta': _rutaController.text.trim(),
      'IDTipo': _tipoController.text.trim(),
    };
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/transport_units/create'),
      headers: {
        'Authorization': 'Bearer ${widget.token}',
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: data,
    );
    setState(() => _loading = false);
    if (response.statusCode == 200 || response.statusCode == 201) {
      widget.onCreated();
    } else {
      setState(() => _error = 'No se pudo crear la unidad.');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: Form(
        key: _formKey,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('Crear Unidad de Transporte', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
            const SizedBox(height: 16),
            TextFormField(
              controller: _idController,
              decoration: InputDecoration(labelText: 'ID'),
              keyboardType: TextInputType.number,
              validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID' : null,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _ubicacionController,
              decoration: InputDecoration(labelText: 'Ubicación'),
              validator: (v) => v == null || v.isEmpty ? 'Ingrese la ubicación' : null,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _capacidadController,
              decoration: InputDecoration(labelText: 'Capacidad'),
              keyboardType: TextInputType.number,
              validator: (v) => v == null || v.isEmpty ? 'Ingrese la capacidad' : null,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _rutaController,
              decoration: InputDecoration(labelText: 'ID Ruta'),
              keyboardType: TextInputType.number,
              validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID de ruta' : null,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _tipoController,
              decoration: InputDecoration(labelText: 'ID Tipo'),
              keyboardType: TextInputType.number,
              validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID de tipo' : null,
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _loading ? null : _submit,
                child: _loading
                    ? SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : Text('Crear'),
              ),
            ),
            if (_error != null) ...[
              const SizedBox(height: 8),
              Text(_error!, style: TextStyle(color: Colors.red)),
            ],
          ],
        ),
      ),
    );
  }
}

// Widget para editar unidad de transporte
class EditarUnidadWidget extends StatefulWidget {
  final String token;
  final Map<String, dynamic> unidad;
  final VoidCallback onUpdated;
  const EditarUnidadWidget({required this.token, required this.unidad, required this.onUpdated, Key? key}) : super(key: key);

  @override
  State<EditarUnidadWidget> createState() => _EditarUnidadWidgetState();
}

class _EditarUnidadWidgetState extends State<EditarUnidadWidget> {
  final _formKey = GlobalKey<FormState>();
  late TextEditingController _idController;
  late TextEditingController _ubicacionController;
  late TextEditingController _capacidadController;
  late TextEditingController _rutaController;
  late TextEditingController _tipoController;
  bool _loading = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    _idController = TextEditingController(text: widget.unidad['ID']?.toString() ?? '');
    _ubicacionController = TextEditingController(text: widget.unidad['Ubicacion']?.toString() ?? '');
    _capacidadController = TextEditingController(text: widget.unidad['Capacidad']?.toString() ?? '');
    _rutaController = TextEditingController(text: widget.unidad['IDRuta']?.toString() ?? '');
    _tipoController = TextEditingController(text: widget.unidad['IDTipo']?.toString() ?? '');
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _loading = true);
    final data = {
      'ID': _idController.text.trim(),
      'Ubicacion': _ubicacionController.text.trim(),
      'Capacidad': _capacidadController.text.trim(),
      'IDRuta': _rutaController.text.trim(),
      'IDTipo': _tipoController.text.trim(),
    };
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/transport_units/update'),
      headers: {
        'Authorization': 'Bearer ${widget.token}',
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: data,
    );
    setState(() => _loading = false);
    if (response.statusCode == 200) {
      widget.onUpdated();
      Navigator.pop(context);
    } else {
      setState(() => _error = 'No se pudo actualizar la unidad.');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: Form(
        key: _formKey,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('Editar Unidad de Transporte', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
            const SizedBox(height: 16),
            TextFormField(
              controller: _idController,
              decoration: InputDecoration(labelText: 'ID'),
              enabled: false,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _ubicacionController,
              decoration: InputDecoration(labelText: 'Ubicación'),
              validator: (v) => v == null || v.isEmpty ? 'Ingrese la ubicación' : null,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _capacidadController,
              decoration: InputDecoration(labelText: 'Capacidad'),
              keyboardType: TextInputType.number,
              validator: (v) => v == null || v.isEmpty ? 'Ingrese la capacidad' : null,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _rutaController,
              decoration: InputDecoration(labelText: 'ID Ruta'),
              keyboardType: TextInputType.number,
              validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID de ruta' : null,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _tipoController,
              decoration: InputDecoration(labelText: 'ID Tipo'),
              keyboardType: TextInputType.number,
              validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID de tipo' : null,
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _loading ? null : _submit,
                child: _loading
                    ? SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : Text('Actualizar'),
              ),
            ),
            if (_error != null) ...[
              const SizedBox(height: 8),
              Text(_error!, style: TextStyle(color: Colors.red)),
            ],
          ],
        ),
      ),
    );
  }
}

// Widgets auxiliares para CRUD de Horarios

enum HorarioFormMode { create, update }

class _HorarioFormWidget extends StatefulWidget {
  final String token;
  final HorarioFormMode mode;
  final VoidCallback onSuccess;
  const _HorarioFormWidget({
    required this.token,
    required this.mode,
    required this.onSuccess,
    Key? key,
  }) : super(key: key);

  @override
  State<_HorarioFormWidget> createState() => _HorarioFormWidgetState();
}

class _HorarioFormWidgetState extends State<_HorarioFormWidget> {
  final _formKey = GlobalKey<FormState>();
  final _idController = TextEditingController();
  final _llegadaController = TextEditingController();
  final _salidaController = TextEditingController();
  bool _loading = false;
  String? _error;
  String? _success;

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _error = null;
      _success = null;
    });
    final data = {
      'id': _idController.text.trim(),
      'Llegada': _llegadaController.text.trim(),
      'Salida': _salidaController.text.trim(),
    };
    final url = widget.mode == HorarioFormMode.create
        ? '${AppConfig.baseUrl}/schedules/create'
        : '${AppConfig.baseUrl}/schedules/update';
    final response = await http.post(
      Uri.parse(url),
      headers: {
        'Authorization': 'Bearer ${widget.token}',
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: data,
    );
    setState(() => _loading = false);
    if (response.statusCode == 200 || response.statusCode == 201) {
      setState(() => _success = widget.mode == HorarioFormMode.create
          ? 'Horario creado exitosamente.'
          : 'Horario actualizado exitosamente.');
      widget.onSuccess();
    } else {
      setState(() => _error = 'Error: ${response.body}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 350,
      child: Form(
        key: _formKey,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              widget.mode == HorarioFormMode.create
                  ? 'Añadir Horario'
                  : 'Actualizar Horario',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _idController,
              decoration: InputDecoration(labelText: 'ID'),
              keyboardType: TextInputType.number,
              validator: (v) =>
                  v == null || v.isEmpty ? 'Ingrese el ID' : null,
              enabled: widget.mode == HorarioFormMode.create,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _llegadaController,
              decoration: InputDecoration(labelText: 'Llegada'),
              validator: (v) =>
                  v == null || v.isEmpty ? 'Ingrese la llegada' : null,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _salidaController,
              decoration: InputDecoration(labelText: 'Salida'),
              validator: (v) =>
                  v == null || v.isEmpty ? 'Ingrese la salida' : null,
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _loading ? null : _submit,
                child: _loading
                    ? SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(
                            strokeWidth: 2, color: Colors.white))
                    : Text(widget.mode == HorarioFormMode.create
                        ? 'Crear'
                        : 'Actualizar'),
              ),
            ),
            if (_success != null) ...[
              const SizedBox(height: 8),
              Text(_success!, style: TextStyle(color: Colors.green)),
            ],
            if (_error != null) ...[
              const SizedBox(height: 8),
              Text(_error!, style: TextStyle(color: Colors.red)),
            ],
          ],
        ),
      ),
    );
  }
}

class _HorarioListWidget extends StatelessWidget {
  final String token;
  const _HorarioListWidget({required this.token, Key? key}) : super(key: key);

  Future<List<dynamic>> fetchHorarios() async {
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/schedules'),
      headers: {
        'Authorization': 'Bearer $token',
        'accept': 'application/json',
      },
    );
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Error al cargar horarios');
    }
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 400,
      child: FutureBuilder<List<dynamic>>(
        future: fetchHorarios(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error al cargar horarios'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return Center(child: Text('No hay horarios registrados.'));
          }
          final horarios = snapshot.data!;
          return ListView.separated(
            shrinkWrap: true,
            itemCount: horarios.length,
            separatorBuilder: (_, __) => Divider(),
            itemBuilder: (_, i) {
              final h = horarios[i];
              return ListTile(
                title: Text('ID: ${h['ID']}'),
                subtitle: Text('Llegada: ${h['Llegada']} | Salida: ${h['Salida']}'),
              );
            },
          );
        },
      ),
    );
  }
}

class _HorarioDeleteWidget extends StatefulWidget {
  final String token;
  final VoidCallback onSuccess;
  const _HorarioDeleteWidget({required this.token, required this.onSuccess, Key? key}) : super(key: key);

  @override
  State<_HorarioDeleteWidget> createState() => _HorarioDeleteWidgetState();
}

class _HorarioDeleteWidgetState extends State<_HorarioDeleteWidget> {
  final _formKey = GlobalKey<FormState>();
  final _idController = TextEditingController();
  bool _loading = false;
  String? _error;
  String? _success;

  Future<void> _delete() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _error = null;
      _success = null;
    });
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/schedules/delete'),
      headers: {
        'Authorization': 'Bearer ${widget.token}',
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: {'id': _idController.text.trim()},
    );
    setState(() => _loading = false);
    if (response.statusCode == 200) {
      setState(() => _success = 'Horario eliminado exitosamente.');
      widget.onSuccess();
    } else {
      setState(() => _error = 'Error: ${response.body}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 300,
      child: Form(
        key: _formKey,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('Eliminar Horario', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
            const SizedBox(height: 16),
            TextFormField(
              controller: _idController,
              decoration: InputDecoration(labelText: 'ID'),
              keyboardType: TextInputType.number,
              validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID' : null,
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _loading ? null : _delete,
                child: _loading
                    ? SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : Text('Eliminar'),
                style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
              ),
            ),
            if (_success != null) ...[
              const SizedBox(height: 8),
              Text(_success!, style: TextStyle(color: Colors.green)),
            ],
            if (_error != null) ...[
              const SizedBox(height: 8),
              Text(_error!, style: TextStyle(color: Colors.red)),
            ],
          ],
        ),
      ),
    );
  }
}

// Widgets auxiliares para CRUD de Rutas

enum RutaFormMode { create, update }

class _RutaFormWidget extends StatefulWidget {
  final String token;
  final RutaFormMode mode;
  final VoidCallback onSuccess;
  const _RutaFormWidget({
    required this.token,
    required this.mode,
    required this.onSuccess,
    Key? key,
  }) : super(key: key);

  @override
  State<_RutaFormWidget> createState() => _RutaFormWidgetState();
}

class _RutaFormWidgetState extends State<_RutaFormWidget> {
  final _formKey = GlobalKey<FormState>();
  final _idController = TextEditingController();
  final _idHorarioController = TextEditingController();
  final _nombreController = TextEditingController();
  bool _loading = false;
  String? _error;
  String? _success;

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _error = null;
      _success = null;
    });
    final data = {
      'ID': _idController.text.trim(),
      'IDHorario': _idHorarioController.text.trim(),
      'Nombre': _nombreController.text.trim(),
    };
    final url = widget.mode == RutaFormMode.create
        ? '${AppConfig.baseUrl}/routes/create'
        : '${AppConfig.baseUrl}/routes/update';
    final response = await http.post(
      Uri.parse(url),
      headers: {
        'Authorization': 'Bearer ${widget.token}',
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: data,
    );
    setState(() => _loading = false);
    if (response.statusCode == 200 || response.statusCode == 201) {
      setState(() => _success = widget.mode == RutaFormMode.create
          ? 'Ruta creada exitosamente.'
          : 'Ruta actualizada exitosamente.');
      widget.onSuccess();
    } else {
      setState(() => _error = 'Error: ${response.body}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 350,
      child: Form(
        key: _formKey,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              widget.mode == RutaFormMode.create
                  ? 'Añadir Ruta'
                  : 'Actualizar Ruta',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _idController,
              decoration: InputDecoration(labelText: 'ID'),
              keyboardType: TextInputType.number,
              validator: (v) =>
                  v == null || v.isEmpty ? 'Ingrese el ID' : null,
              enabled: widget.mode == RutaFormMode.create,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _idHorarioController,
              decoration: InputDecoration(labelText: 'ID Horario'),
              keyboardType: TextInputType.number,
              validator: (v) =>
                  v == null || v.isEmpty ? 'Ingrese el ID Horario' : null,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _nombreController,
              decoration: InputDecoration(labelText: 'Nombre'),
              validator: (v) =>
                  v == null || v.isEmpty ? 'Ingrese el nombre' : null,
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _loading ? null : _submit,
                child: _loading
                    ? SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(
                            strokeWidth: 2, color: Colors.white))
                    : Text(widget.mode == RutaFormMode.create
                        ? 'Crear'
                        : 'Actualizar'),
              ),
            ),
            if (_success != null) ...[
              const SizedBox(height: 8),
              Text(_success!, style: TextStyle(color: Colors.green)),
            ],
            if (_error != null) ...[
              const SizedBox(height: 8),
              Text(_error!, style: TextStyle(color: Colors.red)),
            ],
          ],
        ),
      ),
    );
  }
}

class _RutaListWidget extends StatelessWidget {
  final String token;
  const _RutaListWidget({required this.token, Key? key}) : super(key: key);

  Future<List<dynamic>> fetchRutas() async {
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/routes/'),
      headers: {
        'Authorization': 'Bearer $token',
        'accept': 'application/json',
      },
    );
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Error al cargar rutas');
    }
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 400,
      child: FutureBuilder<List<dynamic>>(
        future: fetchRutas(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error al cargar rutas'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return Center(child: Text('No hay rutas registradas.'));
          }
          final rutas = snapshot.data!;
          return ListView.separated(
            shrinkWrap: true,
            itemCount: rutas.length,
            separatorBuilder: (_, __) => Divider(),
            itemBuilder: (_, i) {
              final r = rutas[i];
              return ListTile(
                title: Text('ID: ${r['ID']}'),
                subtitle: Text('Horario: ${r['IDHorario']} | Nombre: ${r['Nombre']}'),
              );
            },
          );
        },
      ),
    );
  }
}

class _RutaDeleteWidget extends StatefulWidget {
  final String token;
  final VoidCallback onSuccess;
  const _RutaDeleteWidget({required this.token, required this.onSuccess, Key? key}) : super(key: key);

  @override
  State<_RutaDeleteWidget> createState() => _RutaDeleteWidgetState();
}

class _RutaDeleteWidgetState extends State<_RutaDeleteWidget> {
  final _formKey = GlobalKey<FormState>();
  final _idController = TextEditingController();
  bool _loading = false;
  String? _error;
  String? _success;

  Future<void> _delete() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _error = null;
      _success = null;
    });
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/routes/delete'),
      headers: {
        'Authorization': 'Bearer ${widget.token}',
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: {'ID': _idController.text.trim()},
    );
    setState(() => _loading = false);
    if (response.statusCode == 200) {
      setState(() => _success = 'Ruta eliminada exitosamente.');
      widget.onSuccess();
    } else {
      setState(() => _error = 'Error: ${response.body}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 300,
      child: Form(
        key: _formKey,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('Eliminar Ruta', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
            const SizedBox(height: 16),
            TextFormField(
              controller: _idController,
              decoration: InputDecoration(labelText: 'ID'),
              keyboardType: TextInputType.number,
              validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID' : null,
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _loading ? null : _delete,
                child: _loading
                    ? SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : Text('Eliminar'),
                style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
              ),
            ),
            if (_success != null) ...[
              const SizedBox(height: 8),
              Text(_success!, style: TextStyle(color: Colors.green)),
            ],
            if (_error != null) ...[
              const SizedBox(height: 8),
              Text(_error!, style: TextStyle(color: Colors.red)),
            ],
          ],
        ),
      ),
    );
  }
}
// Screen para crear asistencia
class CrearAsistenciaScreen extends StatefulWidget {
  final String token;
  const CrearAsistenciaScreen({Key? key, required this.token})
      : super(key: key);

  static const primaryColor = Color(0xFF1A73E8);

  @override
  State<CrearAsistenciaScreen> createState() =>
      _CrearAsistenciaScreenState();
}

class _CrearAsistenciaScreenState extends State<CrearAsistenciaScreen> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _idController = TextEditingController();
  final TextEditingController _idUserController = TextEditingController();
  final TextEditingController _horaInicioController = TextEditingController();
  final TextEditingController _horaFinalController = TextEditingController();
  final TextEditingController _fechaController = TextEditingController();
  bool _loading = false;
  String? _response;
  String? _error;
  TimeOfDay? _horaInicio;
  TimeOfDay? _horaFinal;
  DateTime? _fechaSeleccionada;

  @override
  void initState() {
    super.initState();
    _fetchNextId();
  }

  String timeOfDayToString(TimeOfDay? t) {
    if (t == null) return '';
    final h = t.hour.toString().padLeft(2, '0');
    final m = t.minute.toString().padLeft(2, '0');
    return "$h:$m:00";
  }

  String dateToString(DateTime? d) {
    if (d == null) return '';
    return "${d.year.toString().padLeft(4, '0')}-${d.month.toString().padLeft(2, '0')}-${d.day.toString().padLeft(2, '0')}";
  }

  Future<void> _selectHoraInicio(BuildContext context) async {
    final TimeOfDay? picked = await showTimePicker(
      context: context,
      initialTime: _horaInicio ?? TimeOfDay.now(),
    );
    if (picked != null) {
      setState(() {
        _horaInicio = picked;
        _horaInicioController.text = picked.format(context);
      });
    }
  }

  Future<void> _selectHoraFinal(BuildContext context) async {
    final TimeOfDay? picked = await showTimePicker(
      context: context,
      initialTime: _horaFinal ?? TimeOfDay.now(),
    );
    if (picked != null) {
      setState(() {
        _horaFinal = picked;
        _horaFinalController.text = picked.format(context);
      });
    }
  }

  Future<void> _selectFecha(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: _fechaSeleccionada ?? DateTime.now(),
      firstDate: DateTime(2000), // Límite inferior (puedes ajustar)
      lastDate: DateTime(2100),  // Límite superior (puedes ajustar)
    );
    if (picked != null) {
      setState(() {
        _fechaSeleccionada = picked;
        _fechaController.text = dateToString(picked);
      });
    }
  }

  Future<void> _fetchNextId() async {
    try {
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/asistance/asistencias'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
        },
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final nextId = (data['count'] ?? 0) + 1;
        setState(() {
          _idController.text = nextId.toString();
        });
      } else {
        setState(() {
          _error = 'No se pudo obtener el siguiente ID. (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión al consultar el ID.';
      });
    }
  }

  Future<void> _crearAsistencia() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _response = null;
      _error = null;
    });
    try {
      final response = await http.post(
        Uri.parse('${AppConfig.baseUrl}/asistance/create'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: {
          'id': _idController.text.trim(),
          'iduser': _idUserController.text.trim(),
          'horainicio': timeOfDayToString(_horaInicio),
          'horafinal': timeOfDayToString(_horaFinal),
          'fecha': dateToString(_fechaSeleccionada),
        },
      );
      if (response.statusCode == 200 || response.statusCode == 201) {
        setState(() {
          _response = 'Asistencia creada exitosamente.';
        });
        _fetchNextId();
      } else {
        setState(() {
          _error = 'No se pudo crear la asistencia. (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión.';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Crear Asistencia'),
        backgroundColor: CrearAsistenciaScreen.primaryColor,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Complete los datos para crear una asistencia:',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 24),
              TextFormField(
                controller: _idController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(
                  labelText: 'ID Asistencia',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.confirmation_number),
                ),
                enabled: false,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _idUserController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(
                  labelText: 'ID Usuario',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.person),
                ),
                validator: (value) => value == null || value.isEmpty
                    ? 'Ingrese el número de Identificación del Usuario'
                    : null,
              ),
              const SizedBox(height: 16),
              GestureDetector(
                onTap: () => _selectHoraInicio(context),
                child: AbsorbPointer(
                  child: TextFormField(
                    controller: _horaInicioController,
                    readOnly: true,
                    decoration: InputDecoration(
                      labelText: 'Hora de Inicio (HH:MM:SS)',
                      border: OutlineInputBorder(),
                      prefixIcon: Icon(Icons.access_time),
                    ),
                    validator: (value) =>
                        value == null || value.isEmpty ? 'Seleccione la hora de inicio' : null,
                  ),
                ),
              ),
              const SizedBox(height: 16),
              GestureDetector(
                onTap: () => _selectHoraFinal(context),
                child: AbsorbPointer(
                  child: TextFormField(
                    controller: _horaFinalController,
                    readOnly: true,
                    decoration: InputDecoration(
                      labelText: 'Hora Final (HH:MM:SS)',
                      border: OutlineInputBorder(),
                      prefixIcon: Icon(Icons.access_time_filled),
                    ),
                    validator: (value) =>
                        value == null || value.isEmpty ? 'Seleccione la hora final' : null,
                  ),
                ),
              ),
              const SizedBox(height: 16),
              GestureDetector(
                onTap: () => _selectFecha(context),
                child: AbsorbPointer(
                  child: TextFormField(
                    controller: _fechaController,
                    readOnly: true,
                    decoration: InputDecoration(
                      labelText: 'Fecha (YYYY-MM-DD)',
                      border: OutlineInputBorder(),
                      prefixIcon: Icon(Icons.date_range),
                    ),
                    validator: (value) =>
                        value == null || value.isEmpty ? 'Seleccione la fecha' : null,
                  ),
                ),
              ),
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _loading ? null : _crearAsistencia,
                  child: _loading
                      ? SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(
                              strokeWidth: 2, color: Colors.white),
                        )
                      : Text('Crear Asistencia'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: CrearAsistenciaScreen.primaryColor,
                    foregroundColor: Colors.white,
                    padding: EdgeInsets.symmetric(vertical: 14),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                ),
              ),
              if (_response != null) ...[
                const SizedBox(height: 24),
                Card(
                  color: Colors.green[50],
                  elevation: 0,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Row(
                      children: [
                        Icon(Icons.check_circle, color: Colors.green[700]),
                        const SizedBox(width: 12),
                        Expanded(
                            child: Text(_response!,
                                style: TextStyle(
                                    color: Colors.green[900],
                                    fontWeight: FontWeight.bold))),
                      ],
                    ),
                  ),
                ),
              ],
              if (_error != null) ...[
                const SizedBox(height: 24),
                Card(
                  color: Colors.red[50],
                  elevation: 0,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Row(
                      children: [
                        Icon(Icons.error, color: Colors.red[700]),
                        const SizedBox(width: 12),
                        Expanded(
                            child: Text(_error!,
                                style: TextStyle(
                                    color: Colors.red[900],
                                    fontWeight: FontWeight.bold))),
                      ],
                    ),
                  ),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}

class CrearUsuarioScreen extends StatefulWidget {
  final String token;
  const CrearUsuarioScreen({Key? key, required this.token}) : super(key: key);

  static const primaryColor = Color(0xFF1A73E8);

  @override
  State<CrearUsuarioScreen> createState() => _CrearUsuarioScreenState();
}

class _CrearUsuarioScreenState extends State<CrearUsuarioScreen> {
  final _formKey = GlobalKey<FormState>();

  // Controladores para los campos
  final TextEditingController _idController = TextEditingController();
  final TextEditingController _identificacionController = TextEditingController();
  final TextEditingController _nombreController = TextEditingController();
  final TextEditingController _apellidoController = TextEditingController();
  final TextEditingController _correoController = TextEditingController();
  final TextEditingController _contrasenaController = TextEditingController();
  final TextEditingController _idTarjetaController = TextEditingController();
  List<Map<String, dynamic>> _turnos = [];
  List<Map<String, dynamic>> _rolusers = [];
  int? _turnoSeleccionado;
  int? _rolSeleccionado;

  bool _loading = false;
  String? _response;
  String? _error;
  @override
  void initState() {
    super.initState();
    _fetchNextId();
    _fetchTurnos();
    _fetchRoles();
  }
  Future<void> _fetchNextId() async {
    try {
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/user/users'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
        },
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final nextId = (data['cantidad'] ?? 0) + 1;
        setState(() {
          _idController.text = nextId.toString();
        });
      } else {
        setState(() {
          _error = 'No se pudo obtener el siguiente ID. (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión al consultar el ID.';
      });
    }
  }
    Future<void> _fetchTurnos() async {
    try {
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/shifts/turnos'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
        },
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        // Ajusta esto según cómo responde tu API
        // Por ejemplo, si tu API retorna {"turnos": [{ID: 1, nombre: "Mañana"}, ...]}
        setState(() {
          _turnos = List<Map<String, dynamic>>.from(data["turnos"] ?? data);
        });
      } else {
        setState(() {
          _error = 'No se pudieron cargar los turnos. (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión al cargar turnos.';
      });
    }
  }

  Future<void> _fetchRoles() async {
    try {
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/roluser/administrador/rolusers'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
        },
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        // Ajusta esto según cómo responde tu API
        // Por ejemplo, si tu API retorna {"roles": [{ID: 1, nombre: "Pasajero"}, ...]}
        setState(() {
          _rolusers = List<Map<String, dynamic>>.from(data["rolusers"] ?? data);
        });
      } else {
        setState(() {
          _error = 'No se pudieron cargar los roles. (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión al cargar roles.';
      });
    }
  }

  Future<void> _crearUsuario() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _response = null;
      _error = null;
    });
    try {
      final response = await http.post(
        Uri.parse('${AppConfig.baseUrl}/user/create'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: {
          'ID': _idController.text.trim(),
          'Identificacion': _identificacionController.text.trim(),
          'Nombre': _nombreController.text.trim(),
          'Apellido': _apellidoController.text.trim(),
          'Correo': _correoController.text.trim(),
          'Contrasena': _contrasenaController.text.trim(),
          'IDRolUsuario': _rolSeleccionado?.toString() ?? '',
          'IDTurno': _turnoSeleccionado?.toString() ?? '',
          'IDTarjeta': _idTarjetaController.text.trim(),
        },
      );
      if (response.statusCode == 200 || response.statusCode == 201) {
        setState(() {
          _response = 'Usuario creado exitosamente.';
        });
        _fetchNextId();
      } else {
        setState(() {
          _error = 'No se pudo crear el usuario. (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión.';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Crear Usuario'),
        backgroundColor: CrearUsuarioScreen.primaryColor,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Complete los datos para crear un usuario:',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 24),

              // Campos del formulario
              TextFormField(
                              controller: _idController,
                              keyboardType: TextInputType.number,
                              decoration: InputDecoration(
                                labelText: 'ID de Usuario',
                                border: OutlineInputBorder(),
                                prefixIcon: Icon(Icons.confirmation_number),
                              ),
                              enabled: false,
                            ),

              TextFormField(
                controller: _identificacionController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(
                  labelText: 'Identificación',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.badge),
                ),
                validator: (v) => v == null || v.isEmpty ? 'Ingrese la identificación' : null,
              ),
              const SizedBox(height: 16),

              TextFormField(
                controller: _nombreController,
                decoration: InputDecoration(
                  labelText: 'Nombre',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.person),
                ),
                validator: (v) => v == null || v.isEmpty ? 'Ingrese el nombre' : null,
              ),
              const SizedBox(height: 16),

              TextFormField(
                controller: _apellidoController,
                decoration: InputDecoration(
                  labelText: 'Apellido',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.person_outline),
                ),
                validator: (v) => v == null || v.isEmpty ? 'Ingrese el apellido' : null,
              ),
              const SizedBox(height: 16),

              TextFormField(
                controller: _correoController,
                decoration: InputDecoration(
                  labelText: 'Correo',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.email),
                ),
                validator: (v) => v == null || v.isEmpty ? 'Ingrese el correo' : null,
              ),
              const SizedBox(height: 16),

              TextFormField(
                controller: _contrasenaController,
                obscureText: true,
                decoration: InputDecoration(
                  labelText: 'Contraseña',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.lock),
                ),
                validator: (v) => v == null || v.isEmpty ? 'Ingrese la contraseña' : null,
              ),

              const SizedBox(height: 16),
              DropdownButtonFormField<int>(
                value: _rolSeleccionado,
                items: _rolusers.map((rol) {
                  return DropdownMenuItem<int>(
                    value: rol["ID"],
                    child: Text(rol["Rol"] ?? rol["Rol"]),
                  );
                }).toList(),
                decoration: InputDecoration(
                  labelText: 'Rol',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.timer),
                ),
                onChanged: (value) {
                  setState(() {
                    _rolSeleccionado = value;
                  });
                },
                validator: (v) =>
                  v == null ? 'Seleccione un rol' : null,
              ),

              const SizedBox(height: 16),
              DropdownButtonFormField<int>(
                value: _turnoSeleccionado,
                items: _turnos.map((turno) {
                  return DropdownMenuItem<int>(
                    value: turno["ID"],
                    child: Text(turno["TipoTurno"] ?? turno["TipoTurno"]),
                  );
                }).toList(),
                decoration: InputDecoration(
                  labelText: 'Turno',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.timer),
                ),
                onChanged: (value) {
                  setState(() {
                    _turnoSeleccionado = value;
                  });
                },
                validator: (v) =>
                  v == null ? 'Seleccione un turno' : null,
              ),

              const SizedBox(height: 16),
              TextFormField(
                controller: _idTarjetaController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(
                  labelText: 'ID Tarjeta',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.credit_card),
                ),
                validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID de tarjeta' : null,
              ),
              const SizedBox(height: 24),

              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _loading ? null : _crearUsuario,
                  child: _loading
                      ? SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(
                              strokeWidth: 2, color: Colors.white),
                        )
                      : Text('Crear Usuario'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: CrearUsuarioScreen.primaryColor,
                    foregroundColor: Colors.white,
                    padding: EdgeInsets.symmetric(vertical: 14),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                ),
              ),
              if (_response != null) ...[
                const SizedBox(height: 24),
                Card(
                  color: Colors.green[50],
                  elevation: 0,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Row(
                      children: [
                        Icon(Icons.check_circle, color: Colors.green[700]),
                        const SizedBox(width: 12),
                        Expanded(
                            child: Text(_response!,
                                style: TextStyle(
                                    color: Colors.green[900],
                                    fontWeight: FontWeight.bold))),
                      ],
                    ),
                  ),
                ),
              ],
              if (_error != null) ...[
                const SizedBox(height: 24),
                Card(
                  color: Colors.red[50],
                  elevation: 0,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Row(
                      children: [
                        Icon(Icons.error, color: Colors.red[700]),
                        const SizedBox(width: 12),
                        Expanded(
                            child: Text(_error!,
                                style: TextStyle(
                                    color: Colors.red[900],
                                    fontWeight: FontWeight.bold))),
                      ],
                    ),
                  ),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
///
///

// Enum para el modo del formulario, por si quieres ampliarlo en el futuro.
enum ActualizarUsuarioFormMode { update }

class UsuarioModel {
  final int id;
  final int identificacion;
  final String nombre;
  final String apellido;
  final String correo;
  final String contrasena;
  final int idRolUsuario;
  final int idTurno;
  final int idTarjeta;

  UsuarioModel({
    required this.id,
    required this.identificacion,
    required this.nombre,
    required this.apellido,
    required this.correo,
    required this.contrasena, 
    required this.idRolUsuario,
    required this.idTurno,
    required this.idTarjeta,
  });

  factory UsuarioModel.fromJson(Map<String, dynamic> json) => UsuarioModel(
    id: json['ID'],
    identificacion: json['Identificacion'],
    nombre: json['Nombre'],
    apellido: json['Apellido'],
    correo: json['Correo'],
    contrasena: json['Contrasena'],
    idRolUsuario: json['IDRolUsuario'],
    idTurno: json['IDTurno'],
    idTarjeta: json['IDTarjeta'],
  );
}

class ActualizarUsuarioScreen  extends StatefulWidget {
  final String token;
  final ActualizarUsuarioFormMode mode;
  final VoidCallback onSuccess;

  const ActualizarUsuarioScreen({
    Key? key,
    required this.token,
    required this.mode,
    required this.onSuccess,
  }) : super(key: key);

  @override
  State<ActualizarUsuarioScreen> createState() => _ActualizarUsuarioScreenState();
}

class _ActualizarUsuarioScreenState extends State<ActualizarUsuarioScreen> {
  final _formKey = GlobalKey<FormState>();
  final _idBusquedaController = TextEditingController();
  bool _mostrarContrasena = false; 

  // Controladores de formulario
  final TextEditingController _idController = TextEditingController();
  final TextEditingController _identificacionController = TextEditingController();
  final TextEditingController _nombreController = TextEditingController();
  final TextEditingController _apellidoController = TextEditingController();
  final TextEditingController _correoController = TextEditingController();
  final TextEditingController _contrasenaController = TextEditingController();
  final TextEditingController _idRolUsuarioController = TextEditingController();
  final TextEditingController _idTarjetaController = TextEditingController();
  final TextEditingController _idTurnoController = TextEditingController();
  List<Map<String, dynamic>> _rolusers = []; 
  int? _rolSeleccionado;
  List<Map<String, dynamic>> _turnos = [];
  int? _turnoSeleccionado;

  bool _loading = false;
  String? _response;
  String? _error;
  bool _userLoaded = false;

  @override
  void initState() {
    super.initState();
    _fetchTurnos();
    _fetchRoles();
  }

  Future<void> _fetchTurnos() async {
    try {
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/shifts/turnos'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
        },
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          _turnos = List<Map<String, dynamic>>.from(data["turnos"] ?? data);
        });
      } else {
        setState(() {
          _error = 'No se pudieron cargar los turnos. (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión al cargar turnos.';
      });
    }
  }
  Future<void> _fetchRoles() async {
    try {
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/roluser/administrador/rolusers'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
        },
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        // Ajusta esto según cómo responde tu API
        // Por ejemplo, si tu API retorna {"roles": [{ID: 1, nombre: "Pasajero"}, ...]}
        setState(() {
          _rolusers = List<Map<String, dynamic>>.from(data["rolusers"] ?? data);
        });
      } else {
        setState(() {
          _error = 'No se pudieron cargar los roles. (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión al cargar roles.';
      });
    }
  }

  Future<void> _buscarUsuario() async {
    setState(() {
      _loading = true;
      _error = null;
      _response = null;
      _userLoaded = false;
    });
    try {
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/user/usuario?id=${_idBusquedaController.text.trim()}'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
        },
      );
      print('URL: ${AppConfig.baseUrl}/user/usuario?id=${_idBusquedaController.text.trim()}');
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final usuario = UsuarioModel.fromJson(data);
        _llenarFormulario(usuario);
        setState(() {
          _userLoaded = true;
        });
      } else {
        setState(() {
          _error = 'Usuario no encontrado (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión al buscar usuario.';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  void _llenarFormulario(UsuarioModel usuario) {
    _idController.text = usuario.id.toString();
    _identificacionController.text = usuario.identificacion.toString();
    _nombreController.text = usuario.nombre;
    _apellidoController.text = usuario.apellido;
    _correoController.text = usuario.correo;
    _idRolUsuarioController.text = usuario.idRolUsuario.toString();
    _idTarjetaController.text = usuario.idTarjeta.toString();
    _idTurnoController.text = usuario.idTurno.toString();
    _contrasenaController.text = usuario.contrasena;
  }

  Future<void> _actualizarUsuario() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _response = null;
      _error = null;
    });
    try {
      final response = await http.post(
        Uri.parse('${AppConfig.baseUrl}/user/update'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: {
          'ID': _idController.text.trim(),
          'Identificacion': _identificacionController.text.trim(),
          'Nombre': _nombreController.text.trim(),
          'Apellido': _apellidoController.text.trim(),
          'Correo': _correoController.text.trim(),
          'Contrasena': _contrasenaController.text.trim(),
          'IDRolUsuario':  _rolSeleccionado?.toString() ?? '',
          'IDTurno': _turnoSeleccionado?.toString() ?? '',
          'IDTarjeta': _idTarjetaController.text.trim(),
        },
      );
      if (response.statusCode == 200 || response.statusCode == 201) {
        setState(() {
          _response = 'Usuario actualizado exitosamente.';
        });
        widget.onSuccess();
      } else {
        setState(() {
          _error = 'No se pudo actualizar el usuario. (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión.';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Paso 1: Campo para buscar usuario
          TextFormField(
            controller: _idBusquedaController,
            decoration: InputDecoration(
              labelText: 'ID del usuario a buscar',
              border: OutlineInputBorder(),
              prefixIcon: Icon(Icons.search),
            ),
            keyboardType: TextInputType.number,
            enabled: !_userLoaded,
          ),
          const SizedBox(height: 8),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              icon: Icon(Icons.search),
              label: Text('Buscar usuario'),
              onPressed: _loading ? null : _buscarUsuario,
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.blue,
                foregroundColor: Colors.white,
              ),
            ),
          ),
          const SizedBox(height: 24),
          if (_userLoaded)
            Form(
              key: _formKey,
              child: Column(
                children: [
                  TextFormField(
                    controller: _idController,
                    keyboardType: TextInputType.number,
                    decoration: InputDecoration(
                      labelText: 'ID de Usuario',
                      border: OutlineInputBorder(),
                      prefixIcon: Icon(Icons.confirmation_number),
                    ),
                    enabled: false,
                  ),
                  const SizedBox(height: 16),
                  TextFormField(
                    controller: _identificacionController,
                    keyboardType: TextInputType.number,
                    decoration: InputDecoration(
                      labelText: 'Identificación',
                      border: OutlineInputBorder(),
                      prefixIcon: Icon(Icons.badge),
                    ),
                    validator: (v) => v == null || v.isEmpty ? 'Ingrese la identificación' : null,
                  ),
                  const SizedBox(height: 16),
                  TextFormField(
                    controller: _nombreController,
                    decoration: InputDecoration(
                      labelText: 'Nombre',
                      border: OutlineInputBorder(),
                      prefixIcon: Icon(Icons.person),
                    ),
                    validator: (v) => v == null || v.isEmpty ? 'Ingrese el nombre' : null,
                  ),
                  const SizedBox(height: 16),
                  TextFormField(
                    controller: _apellidoController,
                    decoration: InputDecoration(
                      labelText: 'Apellido',
                      border: OutlineInputBorder(),
                      prefixIcon: Icon(Icons.person_outline),
                    ),
                    validator: (v) => v == null || v.isEmpty ? 'Ingrese el apellido' : null,
                  ),
                  const SizedBox(height: 16),
                  TextFormField(
                    controller: _correoController,
                    decoration: InputDecoration(
                      labelText: 'Correo',
                      border: OutlineInputBorder(),
                      prefixIcon: Icon(Icons.email),
                    ),
                    validator: (v) => v == null || v.isEmpty ? 'Ingrese el correo' : null,
                  ),
                  const SizedBox(height: 16),
                  TextFormField(
                    controller: _contrasenaController,
                    obscureText: !_mostrarContrasena,
                    decoration: InputDecoration(
                      labelText: 'Contraseña (dejar vacío si no desea cambiarla)',
                      border: OutlineInputBorder(),
                      prefixIcon: Icon(Icons.lock),
                      suffixIcon: IconButton(
                        icon: Icon(
                          _mostrarContrasena ? Icons.visibility : Icons.visibility_off,
                        ),
                        onPressed: () {
                          setState(() {
                            _mostrarContrasena = !_mostrarContrasena;
                          });
                        },
                      ),
                    ),
                    validator: (v) => v == null || v.isEmpty ? 'Contraseña (dejar contraseña si no desea cambiarla)' : null,
                  ),
                
                const SizedBox(height: 16),
                DropdownButtonFormField<int>(
                  value: _rolSeleccionado,
                  items: _rolusers.map((rol) {
                    return DropdownMenuItem<int>(
                      value: rol["ID"],
                      child: Text(rol["Rol"] ?? rol["Rol"]),
                    );
                  }).toList(),
                  decoration: InputDecoration(
                    labelText: 'Rol',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.timer),
                  ),
                  onChanged: (value) {
                    setState(() {
                      _rolSeleccionado = value;
                    });
                  },
                  validator: (v) =>
                    v == null ? 'Seleccione un rol' : null,
                  ),

                  const SizedBox(height: 16),
                  DropdownButtonFormField<int>(
                    value: _turnoSeleccionado,
                    items: _turnos.map((turno) {
                      return DropdownMenuItem<int>(
                        value: turno["ID"],
                        child: Text(turno["TipoTurno"] ?? turno["nombre"] ?? ''),
                      );
                    }).toList(),
                    decoration: InputDecoration(
                      labelText: 'Turno',
                      border: OutlineInputBorder(),
                      prefixIcon: Icon(Icons.timer),
                    ),
                    onChanged: (value) {
                      setState(() {
                        _turnoSeleccionado = value;
                      });
                    },
                    validator: (v) => v == null ? 'Seleccione un turno' : null,
                  ),
                  const SizedBox(height: 16),
                  TextFormField(
                    controller: _idTarjetaController,
                    keyboardType: TextInputType.number,
                    decoration: InputDecoration(
                      labelText: 'ID Tarjeta',
                      border: OutlineInputBorder(),
                      prefixIcon: Icon(Icons.credit_card),
                    ),
                    validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID de tarjeta' : null,
                  ),
                  const SizedBox(height: 24),
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: _loading ? null : _actualizarUsuario,
                      child: _loading
                          ? SizedBox(
                              width: 20,
                              height: 20,
                              child: CircularProgressIndicator(
                                  strokeWidth: 2, color: Colors.white),
                            )
                          : Text('Actualizar Usuario'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.blue,
                        foregroundColor: Colors.white,
                        padding: EdgeInsets.symmetric(vertical: 14),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          if (_response != null) ...[
            const SizedBox(height: 24),
            Card(
              color: Colors.green[50],
              elevation: 0,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Row(
                  children: [
                    Icon(Icons.check_circle, color: Colors.green[700]),
                    const SizedBox(width: 12),
                    Expanded(
                        child: Text(_response!,
                            style: TextStyle(
                                color: Colors.green[900],
                                fontWeight: FontWeight.bold))),
                  ],
                ),
              ),
            ),
          ],
          if (_error != null) ...[
            const SizedBox(height: 24),
            Card(
              color: Colors.red[50],
              elevation: 0,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Row(
                  children: [
                    Icon(Icons.error, color: Colors.red[700]),
                    const SizedBox(width: 12),
                    Expanded(
                        child: Text(_error!,
                            style: TextStyle(
                                color: Colors.red[900],
                                fontWeight: FontWeight.bold))),
                  ],
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }
}
///
///
class CrearUsuarioWidget extends StatefulWidget {
  final String token;
  final VoidCallback onCreated;
  const CrearUsuarioWidget({Key? key, required this.onCreated,required this.token}) : super(key: key);

  static const primaryColor = Color(0xFF1A73E8);

  @override
  State<CrearUsuarioWidget> createState() => _CrearUsuarioWidgetState();
}

class _CrearUsuarioWidgetState extends State<CrearUsuarioWidget> {
  final _formKey = GlobalKey<FormState>();

  // Controladores para los campos
  final TextEditingController _idController = TextEditingController();
  final TextEditingController _identificacionController = TextEditingController();
  final TextEditingController _nombreController = TextEditingController();
  final TextEditingController _apellidoController = TextEditingController();
  final TextEditingController _correoController = TextEditingController();
  final TextEditingController _contrasenaController = TextEditingController();
  final TextEditingController _idTarjetaController = TextEditingController();
  List<Map<String, dynamic>> _turnos = [];
  List<Map<String, dynamic>> _rolusers = [];
  int? _rolSeleccionado;
  int? _turnoSeleccionado;

  bool _loading = false;
  String? _response;
  String? _error;

  @override
  void initState() {
    super.initState();
    _fetchNextId();
    _fetchTurnos();
    _fetchRoles();
  }

  Future<void> _fetchNextId() async {
    try {
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/user/users'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
        },
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final nextId = (data['cantidad'] ?? 0) + 1;
        setState(() {
          _idController.text = nextId.toString();
        });
      } else {
        setState(() {
          _error = 'No se pudo obtener el siguiente ID. (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión al consultar el ID.';
      });
    }
  }

  Future<void> _fetchTurnos() async {
    try {
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/shifts/turnos'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
        },
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          _turnos = List<Map<String, dynamic>>.from(data["turnos"] ?? data);
        });
      } else {
        setState(() {
          _error = 'No se pudieron cargar los turnos. (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión al cargar turnos.';
      });
    }
  }
  Future<void> _fetchRoles() async {
    try {
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/roluser/administrador/rolusers'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
        },
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        // Ajusta esto según cómo responde tu API
        // Por ejemplo, si tu API retorna {"roles": [{ID: 1, nombre: "Pasajero"}, ...]}
        setState(() {
          _rolusers = List<Map<String, dynamic>>.from(data["rolusers"] ?? data);
        });
      } else {
        setState(() {
          _error = 'No se pudieron cargar los roles. (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión al cargar roles.';
      });
    }
  }
  Future<void> _crearUsuario() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _response = null;
      _error = null;
    });
    try {
      final response = await http.post(
        Uri.parse('${AppConfig.baseUrl}/user/create'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: {
          'ID': _idController.text.trim(),
          'Identificacion': _identificacionController.text.trim(),
          'Nombre': _nombreController.text.trim(),
          'Apellido': _apellidoController.text.trim(),
          'Correo': _correoController.text.trim(),
          'Contrasena': _contrasenaController.text.trim(),
          'IDRolUsuario': _rolSeleccionado?.toString() ?? '',
          'IDTurno': _turnoSeleccionado?.toString() ?? '',
          'IDTarjeta': _idTarjetaController.text.trim(),
        },
      );
      if (response.statusCode == 200 || response.statusCode == 201) {
        setState(() {
          _response = 'Usuario creado exitosamente.';
        });
        _fetchNextId();
      } else {
        setState(() {
          _error = 'No se pudo crear el usuario. (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión.';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

@override
Widget build(BuildContext context) {
  return Card(
    elevation: 4,
    margin: const EdgeInsets.all(16.0),
    child: Padding(
      padding: const EdgeInsets.all(24.0),
      child: Form(
        key: _formKey,
        child: LayoutBuilder(
          builder: (context, constraints) {
            return ConstrainedBox(
              constraints: BoxConstraints(
                maxHeight: MediaQuery.of(context).size.height * 0.8,
              ),
              child: SingleChildScrollView(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Complete los datos para crear un usuario:',
                        style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 24),
                    // ...todos tus campos aquí...
                    TextFormField(
                      controller: _idController,
                      keyboardType: TextInputType.number,
                      decoration: InputDecoration(
                        labelText: 'ID de Usuario',
                        border: OutlineInputBorder(),
                        prefixIcon: Icon(Icons.confirmation_number),
                      ),
                      enabled: false,
                    ),
                    const SizedBox(height: 16),
                    TextFormField(
                      controller: _identificacionController,
                      keyboardType: TextInputType.number,
                      decoration: InputDecoration(
                        labelText: 'Identificación',
                        border: OutlineInputBorder(),
                        prefixIcon: Icon(Icons.badge),
                      ),
                      validator: (v) => v == null || v.isEmpty ? 'Ingrese la identificación' : null,
                    ),
                    const SizedBox(height: 16),
                    TextFormField(
                      controller: _nombreController,
                      decoration: InputDecoration(
                        labelText: 'Nombre',
                        border: OutlineInputBorder(),
                        prefixIcon: Icon(Icons.person),
                      ),
                      validator: (v) => v == null || v.isEmpty ? 'Ingrese el nombre' : null,
                    ),
                    const SizedBox(height: 16),
                    TextFormField(
                      controller: _apellidoController,
                      decoration: InputDecoration(
                        labelText: 'Apellido',
                        border: OutlineInputBorder(),
                        prefixIcon: Icon(Icons.person_outline),
                      ),
                      validator: (v) => v == null || v.isEmpty ? 'Ingrese el apellido' : null,
                    ),
                    const SizedBox(height: 16),
                    TextFormField(
                      controller: _correoController,
                      decoration: InputDecoration(
                        labelText: 'Correo',
                        border: OutlineInputBorder(),
                        prefixIcon: Icon(Icons.email),
                      ),
                      validator: (v) => v == null || v.isEmpty ? 'Ingrese el correo' : null,
                    ),
                    const SizedBox(height: 16),
                    TextFormField(
                      controller: _contrasenaController,
                      obscureText: true,
                      decoration: InputDecoration(
                        labelText: 'Contraseña',
                        border: OutlineInputBorder(),
                        prefixIcon: Icon(Icons.lock),
                      ),
                      validator: (v) => v == null || v.isEmpty ? 'Ingrese la contraseña' : null,
                    ),
                    const SizedBox(height: 16),
                    DropdownButtonFormField<int>(
                      value: _rolSeleccionado,
                      items: _rolusers.map((rol) {
                        return DropdownMenuItem<int>(
                          value: rol["ID"],
                          child: Text(rol["Rol"] ?? rol["Rol"]),
                        );
                      }).toList(),
                      decoration: InputDecoration(
                        labelText: 'Rol',
                        border: OutlineInputBorder(),
                        prefixIcon: Icon(Icons.timer),
                      ),
                      onChanged: (value) {
                        setState(() {
                          _rolSeleccionado = value;
                        });
                      },
                      validator: (v) =>
                        v == null ? 'Seleccione un rol' : null,
                      ),
                    const SizedBox(height: 16),
                    DropdownButtonFormField<int>(
                      value: _turnoSeleccionado,
                      items: _turnos.map((turno) {
                        return DropdownMenuItem<int>(
                          value: turno["ID"],
                          child: Text(turno["TipoTurno"] ?? turno["TipoTurno"].toString()),
                        );
                      }).toList(),
                      decoration: InputDecoration(
                        labelText: 'Turno',
                        border: OutlineInputBorder(),
                        prefixIcon: Icon(Icons.timer),
                      ),
                      onChanged: (value) {
                        setState(() {
                          _turnoSeleccionado = value;
                        });
                      },
                      validator: (v) =>
                        v == null ? 'Seleccione un turno' : null,
                    ),
                    const SizedBox(height: 16),
                    TextFormField(
                      controller: _idTarjetaController,
                      keyboardType: TextInputType.number,
                      decoration: InputDecoration(
                        labelText: 'ID Tarjeta',
                        border: OutlineInputBorder(),
                        prefixIcon: Icon(Icons.credit_card),
                      ),
                      validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID de tarjeta' : null,
                    ),
                    const SizedBox(height: 24),
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: _loading ? null : _crearUsuario,
                        child: _loading
                            ? SizedBox(
                                width: 20,
                                height: 20,
                                child: CircularProgressIndicator(
                                    strokeWidth: 2, color: Colors.white),
                              )
                            : Text('Crear Usuario'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: CrearUsuarioWidget.primaryColor,
                          foregroundColor: Colors.white,
                          padding: EdgeInsets.symmetric(vertical: 14),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(12),
                          ),
                        ),
                      ),
                    ),
                    if (_response != null) ...[
                      const SizedBox(height: 24),
                      Card(
                        color: Colors.green[50],
                        elevation: 0,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Padding(
                          padding: const EdgeInsets.all(16.0),
                          child: Row(
                            children: [
                              Icon(Icons.check_circle, color: Colors.green[700]),
                              const SizedBox(width: 12),
                              Expanded(
                                  child: Text(_response!,
                                      style: TextStyle(
                                          color: Colors.green[900],
                                          fontWeight: FontWeight.bold))),
                            ],
                          ),
                        ),
                      ),
                    ],
                    if (_error != null) ...[
                      const SizedBox(height: 24),
                      Card(
                        color: Colors.red[50],
                        elevation: 0,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Padding(
                          padding: const EdgeInsets.all(16.0),
                          child: Row(
                            children: [
                              Icon(Icons.error, color: Colors.red[700]),
                              const SizedBox(width: 12),
                              Expanded(
                                  child: Text(_error!,
                                      style: TextStyle(
                                          color: Colors.red[900],
                                          fontWeight: FontWeight.bold))),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ],
                ),
              ),
            );
          },
        ),
      ),
    ),
  );
}
}
///
///
enum EliminarUsuarioFormMode { normal }

class EliminarUsuarioScreen extends StatefulWidget {
  final String token;
  final EliminarUsuarioFormMode mode;
  final VoidCallback? onSuccess;

  const EliminarUsuarioScreen({
    Key? key,
    required this.token,
    this.mode = EliminarUsuarioFormMode.normal,
    this.onSuccess,
  }) : super(key: key);

  @override
  State<EliminarUsuarioScreen> createState() => _EliminarUsuarioScreenState();
}

class _EliminarUsuarioScreenState extends State<EliminarUsuarioScreen> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _idController = TextEditingController();

  bool _loading = false;
  String? _error;

  Future<void> _confirmarYEliminarUsuario() async {
    final confirm = await showDialog<bool>(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('Confirmar eliminación'),
        content: Text(
            '¿Está seguro que desea eliminar el usuario con ID: ${_idController.text.trim()}? Esta acción no se puede deshacer.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
            onPressed: () => Navigator.of(context).pop(true),
            child: const Text('Eliminar'),
          ),
        ],
      ),
    );
    if (confirm == true) {
      await _eliminarUsuario();
    }
  }

  Future<void> _eliminarUsuario() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _loading = true;
      _error = null;
    });

    try {
      final response = await http.post(
        Uri.parse('${AppConfig.baseUrl}/user/delete'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: {
          'ID': _idController.text.trim(),
        },
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['success'] == true) {
          // Mostrar diálogo de éxito
          await showDialog(
            context: context,
            builder: (_) => AlertDialog(
              title: const Text('Usuario eliminado'),
              content: Text(data['message'] ?? 'Usuario eliminado exitosamente.'),
              actions: [
                TextButton(
                  onPressed: () => Navigator.of(context).pop(),
                  child: const Text('Aceptar'),
                ),
              ],
            ),
          );
          widget.onSuccess?.call();
          setState(() {
            _idController.clear();
          });
        } else {
          setState(() {
            _error = data['message'] ?? 'No se pudo eliminar el usuario.';
          });
        }
      } else if (response.statusCode == 404) {
        setState(() {
          _error = 'Usuario no encontrado.';
        });
      } else {
        setState(() {
          _error = 'Error al eliminar el usuario: (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión.';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  @override
  void dispose() {
    _idController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Form(
            key: _formKey,
            child: Column(
              children: [
                TextFormField(
                  controller: _idController,
                  keyboardType: TextInputType.number,
                  decoration: InputDecoration(
                    labelText: 'ID de Usuario a eliminar',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.delete),
                  ),
                  validator: (v) =>
                      v == null || v.isEmpty ? 'Ingrese el ID del usuario' : null,
                  enabled: !_loading,
                ),
                const SizedBox(height: 24),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    icon: Icon(Icons.delete_forever),
                    label: _loading
                        ? SizedBox(
                            width: 20,
                            height: 20,
                            child: CircularProgressIndicator(
                              strokeWidth: 2,
                              color: Colors.white,
                            ),
                          )
                        : Text('Eliminar Usuario'),
                    onPressed: _loading ? null : _confirmarYEliminarUsuario,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.red,
                      foregroundColor: Colors.white,
                      padding: EdgeInsets.symmetric(vertical: 14),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
          if (_error != null) ...[
            const SizedBox(height: 24),
            Card(
              color: Colors.red[50],
              elevation: 0,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Row(
                  children: [
                    Icon(Icons.error, color: Colors.red[700]),
                    const SizedBox(width: 12),
                    Expanded(
                        child: Text(_error!,
                            style: TextStyle(
                                color: Colors.red[900],
                                fontWeight: FontWeight.bold))),
                  ],
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }
}
/// Widget para consultar un usuario por ID utilizando el endpoint /user/usuario
class ConsultarUsuarioScreen extends StatefulWidget {
  final String token;
  final VoidCallback? onSuccess;
  const ConsultarUsuarioScreen({Key? key, required this.onSuccess, required this.token}) : super(key: key);

  @override
  State<ConsultarUsuarioScreen> createState() => _ConsultarUsuarioScreenState();
}

class _ConsultarUsuarioScreenState extends State<ConsultarUsuarioScreen> {
  final _idController = TextEditingController();
  bool _loading = false;
  String? _error;
  Map<String, dynamic>? _usuario;

  Future<void> _consultarUsuario() async {
    setState(() {
      _loading = true;
      _error = null;
      _usuario = null;
    });

    try {
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/user/usuario?id=${_idController.text.trim()}'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          _usuario = data;
        });
      } else if (response.statusCode == 404) {
        setState(() {
          _error = "Usuario no encontrado.";
        });
      } else {
        setState(() {
          _error = "Error al consultar el usuario: (${response.body})";
        });
      }
    } catch (e) {
      setState(() {
        _error = "Error de conexión.";
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  @override
  void dispose() {
    _idController.dispose();
    super.dispose();
  }

  Widget _usuarioCard(Map<String, dynamic> usuario) {
    return Card(
      margin: const EdgeInsets.only(top: 24),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: usuario.entries.map((entry) {
            return Padding(
              padding: const EdgeInsets.symmetric(vertical: 4),
              child: Row(
                children: [
                  Text(
                    "${entry.key}: ",
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                  Expanded(child: Text("${entry.value}")),
                ],
              ),
            );
          }).toList(),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            TextFormField(
              controller: _idController,
              decoration: InputDecoration(
                labelText: 'ID de Usuario',
                border: const OutlineInputBorder(),
                prefixIcon: const Icon(Icons.search),
              ),
              keyboardType: TextInputType.number,
              enabled: !_loading,
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                icon: const Icon(Icons.search),
                label: _loading
                    ? const SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                          color: Colors.white,
                        ),
                      )
                    : const Text('Consultar Usuario'),
                onPressed: _loading ? null : _consultarUsuario,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.blue,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ),
            ),
            if (_usuario != null) _usuarioCard(_usuario!),
            if (_error != null) ...[
              const SizedBox(height: 24),
              Card(
                color: Colors.red[50],
                elevation: 0,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Row(
                    children: [
                      Icon(Icons.error, color: Colors.red[700]),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Text(_error!,
                            style: TextStyle(
                                color: Colors.red[900],
                                fontWeight: FontWeight.bold)),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
///
///
///PQR CRUD SERVICE
// MODELO
class PqrModel {
  final String? id;
  final String? iduser;
  final String? tipo;
  final String? descripcion;
  final String? fecha;

  PqrModel({
    this.id,
    this.iduser,
    this.tipo,
    this.descripcion,
    this.fecha,
  });

  factory PqrModel.fromJson(Map<String, dynamic> json) {
    return PqrModel(
      id: json['ID']?.toString(),
      iduser: json['iduser']?.toString(),
      tipo: json['tipo'],
      descripcion: json['descripcion'],
      fecha: json['fecha'],
    );
  }

  Map<String, String> toFormData() {
    return {
      if (id != null) 'ID': id!,
      if (iduser != null) 'iduser': iduser!,
      if (tipo != null) 'tipo': tipo!,
      if (descripcion != null) 'descripcion': descripcion!,
      if (fecha != null) 'fecha': fecha!,
    };
  }
}

// SERVICIO API
class PqrApiService {
  final String token;
  static const String _defaultBaseUrl = AppConfig.baseUrl;

  PqrApiService({required this.token});
  String get baseUrl => _defaultBaseUrl;

  Map<String, String> get _headers => {
    'Authorization': 'Bearer $token',
    'accept': 'application/json',
  };

  Map<String, String> get _formHeaders => {
    ..._headers,
    'Content-Type': 'application/x-www-form-urlencoded',
  };

  Future<ApiResponse<int>> getNextId() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/pqr/administrador/pqrs'),
        headers: _headers,
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final pqrs = (data['pqrs'] as List?) ?? [];
        int nextId = 1;
        if (pqrs.isNotEmpty) {
          final ids = pqrs.map((e) => int.tryParse(e['ID'].toString()) ?? 0).toList();
          nextId = (ids.isNotEmpty ? (ids.reduce((a, b) => a > b ? a : b)) : 0) + 1;
        }
        return ApiResponse.success(nextId);
      } else {
        return ApiResponse.error('No se pudo obtener el siguiente ID');
      }
    } catch (e) {
      return ApiResponse.error('Error de conexión al consultar el ID');
    }
  }

  Future<ApiResponse<String>> createPqr(PqrModel pqr) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/pqr/create'),
        headers: _formHeaders,
        body: pqr.toFormData(),
      );
      if (response.statusCode == 201 || response.statusCode == 200) {
        return ApiResponse.success('PQR creada exitosamente');
      } else {
        return ApiResponse.error('No se pudo crear la PQR: ${response.body}');
      }
    } catch (e) {
      return ApiResponse.error('Error de conexión al crear PQR');
    }
  }

  Future<ApiResponse<String>> updatePqr(PqrModel pqr) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/pqr/update'),
        headers: _formHeaders,
        body: pqr.toFormData(),
      );
      if (response.statusCode == 200) {
        return ApiResponse.success('PQR actualizada exitosamente');
      } else {
        return ApiResponse.error('No se pudo actualizar la PQR: ${response.body}');
      }
    } catch (e) {
      return ApiResponse.error('Error de conexión al actualizar PQR');
    }
  }

  Future<ApiResponse<String>> deletePqr(String id) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/pqr/delete'),
        headers: _formHeaders,
        body: {'ID': id},
      );
      if (response.statusCode == 200) {
        return ApiResponse.success('PQR eliminada exitosamente');
      } else {
        return ApiResponse.error('No se pudo eliminar la PQR: ${response.body}');
      }
    } catch (e) {
      return ApiResponse.error('Error de conexión al eliminar PQR');
    }
  }

  Future<ApiResponse<List<PqrModel>>> getAllPqrs() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/pqr/administrador/pqrs'),
        headers: _headers,
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final pqrs = (data['pqrs'] as List?)
            ?.map((json) => PqrModel.fromJson(json))
            .toList() ?? [];
        return ApiResponse.success(pqrs);
      } else {
        return ApiResponse.error('Error al cargar PQRs: ${response.body}');
      }
    } catch (e) {
      return ApiResponse.error('Error de conexión al cargar PQRs');
    }
  }

  Future<ApiResponse<List<PqrModel>>> getPqrsByUser(String iduser) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/pqr/byuser?iduser=$iduser'),
        headers: _headers,
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final pqrs = (data['pqrs'] as List?)
            ?.map((json) => PqrModel.fromJson(json))
            .toList() ?? [];
        return ApiResponse.success(pqrs);
      } else {
        return ApiResponse.error('No se encontraron PQRs para ese usuario');
      }
    } catch (e) {
      return ApiResponse.error('Error de conexión al buscar PQRs del usuario');
    }
  }
}

// RESPUESTA API
class ApiResponse<T> {
  final T? data;
  final String? error;
  final bool isSuccess;

  ApiResponse._({this.data, this.error, required this.isSuccess});

  factory ApiResponse.success(T data) {
    return ApiResponse._(data: data, isSuccess: true);
  }

  factory ApiResponse.error(String error) {
    return ApiResponse._(error: error, isSuccess: false);
  }
}

// CONTROLADOR DE FORMULARIO
class PqrFormController {
  final GlobalKey<FormState> formKey = GlobalKey<FormState>();
  final TextEditingController idController = TextEditingController();
  final TextEditingController iduserController = TextEditingController();
  final TextEditingController tipoController = TextEditingController();
  final TextEditingController descripcionController = TextEditingController();
  final TextEditingController fechaController = TextEditingController();

  void clear() {
    idController.clear();
    iduserController.clear();
    tipoController.clear();
    descripcionController.clear();
    fechaController.clear();
  }

  void dispose() {
    idController.dispose();
    iduserController.dispose();
    tipoController.dispose();
    descripcionController.dispose();
    fechaController.dispose();
  }
}

enum MessageType { success, error }

// TIPOS DE PQR
const List<String> kTipoPqrOptions = [
  "Petición",
  "Queja",
  "Reclamo",
  "Sugerencia",
  "Felicitación",
  "Otro",
];

// WIDGET PRINCIPAL
class PqrCrudWidget extends StatefulWidget {
  final String token;
  final VoidCallback? onSuccess;
  final VoidCallback? onBack;

  const PqrCrudWidget({
    Key? key,
    required this.token,
    this.onSuccess,
    this.onBack,
  }) : super(key: key);

  @override
  State<PqrCrudWidget> createState() => _PqrCrudWidgetState();
}

class _PqrCrudWidgetState extends State<PqrCrudWidget>
    with TickerProviderStateMixin, AutomaticKeepAliveClientMixin {
  late TabController _tabController;
  late PqrApiService _apiService;
  bool _isLoading = false;
  String? _message;
  String? _lastLoadedId;
  MessageType? _messageType;

  List<PqrModel> _allPqrs = [];
  List<PqrModel> _userPqrs = [];

  final Map<String, PqrFormController> _formControllers = {};

  @override
  bool get wantKeepAlive => true;

    @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 5, vsync: this);
    _apiService = PqrApiService(token: widget.token);
    _formControllers['create'] = PqrFormController();
    _formControllers['update'] = PqrFormController();
    _formControllers['delete'] = PqrFormController();
    _formControllers['findByUser'] = PqrFormController();
    _initializeData();
  }

  Future<void> _initializeData() async {
    await Future.wait([
      _loadNextId(),
      _loadAllPqrs(),
    ]);
  }

  Future<void> _loadNextId() async {
    final response = await _apiService.getNextId();
    if (response.isSuccess && response.data != null) {
      setState(() {
        _formControllers['create']?.idController.text = response.data.toString();
        _lastLoadedId = response.data.toString(); // <--- fuerza rebuild
      });
    }
  }
  Future<void> _createPqr() async {
    final controller = _formControllers['create']!;
    if (!controller.formKey.currentState!.validate()) return;
    setState(() => _isLoading = true);
    final pqr = PqrModel(
      id: controller.idController.text.trim(),
      iduser: controller.iduserController.text.trim(),
      tipo: controller.tipoController.text.trim(),
      descripcion: controller.descripcionController.text.trim(),
      fecha: controller.fechaController.text.trim(),
    );
    final response = await _apiService.createPqr(pqr);
    setState(() => _isLoading = false);
    if (response.isSuccess) {
      controller.clear();
      await Future.wait([_loadNextId(), _loadAllPqrs()]);
      widget.onSuccess?.call();
    }
  }

  Future<void> _updatePqr() async {
    final controller = _formControllers['update']!;
    if (!controller.formKey.currentState!.validate()) return;
    setState(() => _isLoading = true);
    final pqr = PqrModel(
      id: controller.idController.text.trim(),
      iduser: controller.iduserController.text.trim(),
      tipo: controller.tipoController.text.trim(),
      descripcion: controller.descripcionController.text.trim(),
      fecha: controller.fechaController.text.trim(),
    );
    final response = await _apiService.updatePqr(pqr);
    setState(() => _isLoading = false);
    if (response.isSuccess) {
      await _loadAllPqrs();
    }
  }

  Future<void> _deletePqr() async {
    final controller = _formControllers['delete']!;
    if (!controller.formKey.currentState!.validate()) return;
    final confirmed = await _showDeleteConfirmation();
    if (!confirmed) return;
    setState(() => _isLoading = true);
    final response = await _apiService.deletePqr(controller.idController.text.trim());
    setState(() => _isLoading = false);
    if (response.isSuccess) {
      controller.clear();
      await Future.wait([_loadNextId(), _loadAllPqrs()]);
    }
  }

  Future<bool> _showDeleteConfirmation() async {
    return await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Confirmar eliminación'),
        content: const Text('¿Está seguro de que desea eliminar esta PQR?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.of(context).pop(true),
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
            child: const Text('Eliminar'),
          ),
        ],
      ),
    ) ?? false;
  }

  Future<void> _loadAllPqrs() async {
    setState(() => _isLoading = true);
    final response = await _apiService.getAllPqrs();
    setState(() {
      _isLoading = false;
      if (response.isSuccess) {
        _allPqrs = response.data ?? [];
      }
    });
  }

  Future<void> _findPqrsByUser() async {
    final controller = _formControllers['findByUser']!;
    if (!controller.formKey.currentState!.validate()) return;
    setState(() => _isLoading = true);
    final response = await _apiService.getPqrsByUser(controller.iduserController.text.trim());
    setState(() {
      _isLoading = false;
      if (response.isSuccess) {
        _userPqrs = response.data ?? [];
      }
    });
  }

  Future<void> _selectDate(TextEditingController controller) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime(2020),
      lastDate: DateTime(2030),
    );
    if (picked != null) {
      controller.text = picked.toString().split(' ')[0];
    }
  }

  @override
  Widget build(BuildContext context) {
    super.build(context);
    return Scaffold(
      appBar: AppBar(
        title: const Text('Gestión de PQRs'),
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
        elevation: 2,
        leading: widget.onBack != null
            ? IconButton(
                icon: const Icon(Icons.arrow_back),
                onPressed: widget.onBack,
              )
            : null,
        bottom: TabBar(
          controller: _tabController,
          isScrollable: true,
          indicatorColor: Colors.white,
          labelColor: Colors.white,
          unselectedLabelColor: Colors.white70,
          tabs: const [
            Tab(icon: Icon(Icons.add), text: 'Crear'),
            Tab(icon: Icon(Icons.edit), text: 'Actualizar'),
            Tab(icon: Icon(Icons.delete), text: 'Eliminar'),
            Tab(icon: Icon(Icons.list), text: 'Todas'),
            Tab(icon: Icon(Icons.person_search), text: 'Por Usuario'),
          ],
        ),
      ),
      body: Column(
        children: [
          if (_message != null) _buildMessageBanner(),
          Expanded(
            child: TabBarView(
              controller: _tabController,
              children: [
                _buildFormTab('create', _createPqr, 'Crear PQR', Colors.blue, isCreate: true),
                _buildFormTab('update', _updatePqr, 'Actualizar PQR', Colors.purple),
                _buildDeleteTab(),
                _buildAllPqrsTab(),
                _buildPqrsByUserTab(),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMessageBanner() {
    final isError = _messageType == MessageType.error;
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      color: isError ? Colors.red[50] : Colors.green[50],
      child: Row(
        children: [
          Icon(
            isError ? Icons.error : Icons.check_circle,
            color: isError ? Colors.red[700] : Colors.green[700],
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              _message!,
              style: TextStyle(
                color: isError ? Colors.red[900] : Colors.green[900],
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.close),
            onPressed: () => setState(() {
              _message = null;
              _messageType = null;
            }),
          ),
        ],
      ),
    );
  }

  Widget _buildFormTab(
    String formKey,
    VoidCallback onSubmit,
    String buttonText,
    Color buttonColor, {
    bool isCreate = false,
  }) {
    final controller = _formControllers[formKey]!;
    return Form(
      key: controller.formKey,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          const SizedBox(height: 16),
          CustomTextFormField(
            controller: controller.idController,
            label: 'ID',
            keyboardType: TextInputType.number,
            enabled: isCreate ? false : true, // Solo lectura en crear
            validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID' : null,
          ),
          const SizedBox(height: 16),
          CustomTextFormField(
            controller: controller.iduserController,
            label: 'ID Usuario',
            keyboardType: TextInputType.number,
            validator: (v) => v == null || v.isEmpty ? 'Ingrese el número de Identificación del usuario' : null,
          ),
          const SizedBox(height: 16),
          // Menú desplegable para tipo
          CustomDropdownFormField(
            controller: controller.tipoController,
            label: 'Tipo',
            items: kTipoPqrOptions,
            validator: (v) => v == null || v.isEmpty ? 'Seleccione el tipo de PQR' : null,
          ),
          const SizedBox(height: 16),
          CustomTextFormField(
            controller: controller.descripcionController,
            label: 'Descripción',
            keyboardType: TextInputType.text,
            validator: (v) => v == null || v.isEmpty ? 'Ingrese la descripción' : null,
          ),
          const SizedBox(height: 16),
          CustomDateField(
            controller: controller.fechaController,
            label: 'Fecha',
            onTap: () => _selectDate(controller.fechaController),
            validator: (v) => v == null || v.isEmpty ? 'Seleccione la fecha' : null,
          ),
          const SizedBox(height: 32),
          CustomElevatedButton(
            onPressed: _isLoading ? null : onSubmit,
            backgroundColor: buttonColor,
            isLoading: _isLoading,
            child: Text(buttonText),
          ),
        ],
      ),
    );
  }

  Widget _buildDeleteTab() {
    final controller = _formControllers['delete']!;
    return Form(
      key: controller.formKey,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          CustomTextFormField(
            controller: controller.idController,
            label: 'ID a eliminar',
            keyboardType: TextInputType.number,
            validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID a eliminar' : null,
          ),
          const SizedBox(height: 32),
          CustomElevatedButton(
            onPressed: _isLoading ? null : _deletePqr,
            backgroundColor: Colors.red,
            isLoading: _isLoading,
            child: const Text('Eliminar PQR'),
          ),
        ],
      ),
    );
  }

  Widget _buildAllPqrsTab() {
    if (_isLoading && _allPqrs.isEmpty) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_allPqrs.isEmpty) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.inbox, size: 64, color: Colors.grey),
            SizedBox(height: 16),
            Text('No hay PQRs registradas', style: TextStyle(fontSize: 18, color: Colors.grey)),
          ],
        ),
      );
    }
    return RefreshIndicator(
      onRefresh: _loadAllPqrs,
      child: ListView.builder(
        padding: const EdgeInsets.all(8),
        itemCount: _allPqrs.length,
        itemBuilder: (context, index) {
          final pqr = _allPqrs[index];
          return PqrCard(pqr: pqr);
        },
      ),
    );
  }

  Widget _buildPqrsByUserTab() {
    final controller = _formControllers['findByUser']!;
    return Form(
      key: controller.formKey,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          CustomTextFormField(
            controller: controller.iduserController,
            label: 'ID Usuario',
            keyboardType: TextInputType.number,
            validator: (v) => v == null || v.isEmpty ? 'Ingrese el número de Identificación de usuario' : null,
          ),
          const SizedBox(height: 16),
          CustomElevatedButton(
            onPressed: _isLoading ? null : _findPqrsByUser,
            backgroundColor: Colors.blue,
            isLoading: _isLoading,
            child: const Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(Icons.person_search),
                SizedBox(width: 8),
                Text('Buscar'),
              ],
            ),
          ),
          const SizedBox(height: 24),
          if (_userPqrs.isEmpty && !_isLoading)
            const Text(
              'No hay PQRs para ese usuario.',
              style: TextStyle(color: Colors.grey),
            ),
          ..._userPqrs.map((pqr) => Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: PqrCard(pqr: pqr),
          )),
        ],
      ),
    );
  }
}

// WIDGETS PERSONALIZADOS
class CustomTextFormField extends StatelessWidget {
  final TextEditingController controller;
  final String label;
  final TextInputType? keyboardType;
  final bool enabled;
  final String? Function(String?)? validator;

  const CustomTextFormField({
    Key? key,
    required this.controller,
    required this.label,
    this.keyboardType,
    this.enabled = true,
    this.validator,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      controller: controller,
      keyboardType: keyboardType,
      enabled: enabled,
      decoration: InputDecoration(
        labelText: label,
        border: const OutlineInputBorder(),
        filled: !enabled,
        fillColor: enabled ? null : Colors.grey[100],
      ),
      validator: validator,
    );
  }
}

class CustomDropdownFormField extends StatelessWidget {
  final TextEditingController controller;
  final String label;
  final List<String> items;
  final String? Function(String?)? validator;

  const CustomDropdownFormField({
    Key? key,
    required this.controller,
    required this.label,
    required this.items,
    this.validator,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return DropdownButtonFormField<String>(
      value: controller.text.isNotEmpty && items.contains(controller.text) ? controller.text : null,
      items: items
          .map((item) => DropdownMenuItem<String>(
                value: item,
                child: Text(item),
              ))
          .toList(),
      onChanged: (value) {
        controller.text = value ?? '';
      },
      decoration: InputDecoration(
        labelText: label,
        border: const OutlineInputBorder(),
      ),
      validator: validator,
    );
  }
}

class CustomDateField extends StatelessWidget {
  final TextEditingController controller;
  final String label;
  final VoidCallback onTap;
  final String? Function(String?)? validator;

  const CustomDateField({
    Key? key,
    required this.controller,
    required this.label,
    required this.onTap,
    this.validator,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      controller: controller,
      readOnly: true,
      decoration: InputDecoration(
        labelText: label,
        border: const OutlineInputBorder(),
        suffixIcon: const Icon(Icons.calendar_today),
      ),
      onTap: onTap,
      validator: validator,
    );
  }
}

class CustomElevatedButton extends StatelessWidget {
  final VoidCallback? onPressed;
  final Widget child;
  final Color backgroundColor;
  final bool isLoading;

  const CustomElevatedButton({
    Key? key,
    required this.onPressed,
    required this.child,
    required this.backgroundColor,
    this.isLoading = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: double.infinity,
      height: 48,
      child: ElevatedButton(
        onPressed: onPressed,
        style: ElevatedButton.styleFrom(
          backgroundColor: backgroundColor,
          foregroundColor: Colors.white,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
        child: isLoading
            ? const SizedBox(
                width: 20,
                height: 20,
                child: CircularProgressIndicator(
                  strokeWidth: 2,
                  color: Colors.white,
                ),
              )
            : child,
      ),
    );
  }
}

class PqrCard extends StatelessWidget {
  final PqrModel pqr;

  const PqrCard({Key? key, required this.pqr}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 2,
      margin: const EdgeInsets.symmetric(vertical: 4),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Text(
                  'ID: ${pqr.id ?? 'N/A'}',
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    color: Colors.grey,
                  ),
                ),
                const Spacer(),
                Text(
                  pqr.fecha ?? 'Sin fecha',
                  style: TextStyle(color: Colors.grey[700]),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text('Usuario: ${pqr.iduser ?? 'N/A'}'),
            Text('Tipo: ${pqr.tipo ?? 'N/A'}'),
            Text('Descripción: ${pqr.descripcion ?? 'N/A'}'),
          ],
        ),
      ),
    );
  }
}
////
///
///
// Widget para asignar ruta a una unidad (solo permite modificar IDRuta)
class AsignarRutaUnidadWidget extends StatefulWidget {
  final String token;
  final Map<String, dynamic> unidad;
  final VoidCallback onUpdated;
  const AsignarRutaUnidadWidget({required this.token, required this.unidad, required this.onUpdated, Key? key}) : super(key: key);

  @override
  State<AsignarRutaUnidadWidget> createState() => _AsignarRutaUnidadWidgetState();
}

class _AsignarRutaUnidadWidgetState extends State<AsignarRutaUnidadWidget> {
  final _formKey = GlobalKey<FormState>();
  late TextEditingController _idController;
  late TextEditingController _ubicacionController;
  late TextEditingController _capacidadController;
  late TextEditingController _rutaController;
  late TextEditingController _tipoController;
  bool _loading = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    _idController = TextEditingController(text: widget.unidad['ID']?.toString() ?? '');
    _ubicacionController = TextEditingController(text: widget.unidad['Ubicacion']?.toString() ?? '');
    _capacidadController = TextEditingController(text: widget.unidad['Capacidad']?.toString() ?? '');
    _rutaController = TextEditingController(text: widget.unidad['IDRuta']?.toString() ?? '');
    _tipoController = TextEditingController(text: widget.unidad['IDTipo']?.toString() ?? '');
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _loading = true);
    final data = {
      'ID': _idController.text.trim(),
      'Ubicacion': _ubicacionController.text.trim(),
      'Capacidad': _capacidadController.text.trim(),
      'IDRuta': _rutaController.text.trim(), // Solo este puede cambiar
      'IDTipo': _tipoController.text.trim(),
    };
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/transport_units/update'),
      headers: {
        'Authorization': 'Bearer ${widget.token}',
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: data,
    );
    setState(() => _loading = false);
    if (response.statusCode == 200) {
      widget.onUpdated();
      Navigator.pop(context);
    } else {
      setState(() => _error = 'No se pudo asignar la ruta.');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: Form(
        key: _formKey,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('Asignar Ruta a Unidad', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
            const SizedBox(height: 16),
            TextFormField(
              controller: _idController,
              decoration: InputDecoration(labelText: 'ID'),
              enabled: false,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _ubicacionController,
              decoration: InputDecoration(labelText: 'Ubicación'),
              enabled: false,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _capacidadController,
              decoration: InputDecoration(labelText: 'Capacidad'),
              enabled: false,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _rutaController,
              decoration: InputDecoration(labelText: 'ID Ruta'),
              keyboardType: TextInputType.number,
              validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID de ruta' : null,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _tipoController,
              decoration: InputDecoration(labelText: 'ID Tipo'),
              enabled: false,
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _loading ? null : _submit,
                child: _loading
                    ? SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : Text('Asignar Ruta'),
              ),
            ),
            if (_error != null) ...[
              const SizedBox(height: 8),
              Text(_error!, style: TextStyle(color: Colors.red)),
            ],
          ],
        ),
      ),
    );
  }
}
///
/// Rendimiento Widget
// MODELO
class BehaviorModel {
  final String? id;
  final String? iduser;
  final String? cantidadrutas;
  final String? horastrabajadas;
  final String? observaciones;
  final String? fecha;

  BehaviorModel({
    this.id,
    this.iduser,
    this.cantidadrutas,
    this.horastrabajadas,
    this.observaciones,
    this.fecha,
  });

  factory BehaviorModel.fromJson(Map<String, dynamic> json) {
    return BehaviorModel(
      id: json['ID']?.toString(),
      iduser: json['iduser']?.toString(),
      cantidadrutas: json['cantidadrutas']?.toString(),
      horastrabajadas: json['horastrabajadas']?.toString(),
      observaciones: json['observaciones'],
      fecha: json['fecha'],
    );
  }

  Map<String, String> toFormData() {
    return {
      if (id != null) 'ID': id!,
      if (iduser != null) 'iduser': iduser!,
      if (cantidadrutas != null) 'cantidadrutas': cantidadrutas!,
      if (horastrabajadas != null) 'horastrabajadas': horastrabajadas!,
      if (observaciones != null) 'observaciones': observaciones!,
      if (fecha != null) 'fecha': fecha!,
    };
  }
}

// SERVICIO API
class BehaviorApiService {
  final String token;
  static const String _defaultBaseUrl = AppConfig.baseUrl;

  BehaviorApiService({required this.token});
  String get baseUrl => _defaultBaseUrl;

  Map<String, String> get _headers => {
    'Authorization': 'Bearer $token',
    'accept': 'application/json',
  };

  Map<String, String> get _formHeaders => {
    ..._headers,
    'Content-Type': 'application/x-www-form-urlencoded',
  };

  Future<ApiResponse<int>> getNextId() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/behavior/rendimientos'),
        headers: _headers,
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final rendimientos = (data['rendimientos'] as List?) ?? [];
        int nextId = 1;
        if (rendimientos.isNotEmpty) {
          final ids = rendimientos.map((e) => int.tryParse(e['ID'].toString()) ?? 0).toList();
          nextId = (ids.isNotEmpty ? (ids.reduce((a, b) => a > b ? a : b)) : 0) + 1;
        }
        return ApiResponse.success(nextId);
      } else {
        return ApiResponse.error('No se pudo obtener el siguiente ID');
      }
    } catch (e) {
      return ApiResponse.error('Error de conexión al consultar el ID');
    }
  }

  Future<ApiResponse<String>> createBehavior(BehaviorModel behavior) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/behavior/create'),
        headers: _formHeaders,
        body: behavior.toFormData(),
      );
      if (response.statusCode == 201 || response.statusCode == 200) {
        return ApiResponse.success('Rendimiento creado exitosamente');
      } else {
        return ApiResponse.error('No se pudo crear el rendimiento: ${response.body}');
      }
    } catch (e) {
      return ApiResponse.error('Error de conexión al crear rendimiento');
    }
  }

  Future<ApiResponse<String>> updateBehavior(BehaviorModel behavior) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/behavior/update'),
        headers: _formHeaders,
        body: behavior.toFormData(),
      );
      if (response.statusCode == 200) {
        return ApiResponse.success('Rendimiento actualizado exitosamente');
      } else {
        return ApiResponse.error('No se pudo actualizar el rendimiento: ${response.body}');
      }
    } catch (e) {
      return ApiResponse.error('Error de conexión al actualizar rendimiento');
    }
  }

  Future<ApiResponse<String>> deleteBehavior(String id) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/behavior/delete'),
        headers: _formHeaders,
        body: {'ID': id},
      );
      if (response.statusCode == 200) {
        return ApiResponse.success('Rendimiento eliminado exitosamente');
      } else {
        return ApiResponse.error('No se pudo eliminar el rendimiento: ${response.body}');
      }
    } catch (e) {
      return ApiResponse.error('Error de conexión al eliminar rendimiento');
    }
  }

  Future<ApiResponse<List<BehaviorModel>>> getAllBehaviors() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/behavior/rendimientos'),
        headers: _headers,
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final behaviors = (data['rendimientos'] as List?)
            ?.map((json) => BehaviorModel.fromJson(json))
            .toList() ?? [];
        return ApiResponse.success(behaviors);
      } else {
        return ApiResponse.error('Error al cargar rendimientos: ${response.body}');
      }
    } catch (e) {
      return ApiResponse.error('Error de conexión al cargar rendimientos');
    }
  }

  Future<ApiResponse<List<BehaviorModel>>> getBehaviorsByUser(String iduser) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/behavior/byuser?iduser=$iduser'),
        headers: _headers,
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final behaviors = (data['rendimientos'] as List?)
            ?.map((json) => BehaviorModel.fromJson(json))
            .toList() ?? [];
        return ApiResponse.success(behaviors);
      } else {
        return ApiResponse.error('No se encontraron rendimientos para ese usuario');
      }
    } catch (e) {
      return ApiResponse.error('Error de conexión al buscar rendimientos del usuario');
    }
  }
}
// CONTROLADOR DE FORMULARIO
class BehaviorFormController {
  final GlobalKey<FormState> formKey = GlobalKey<FormState>();
  final TextEditingController idController = TextEditingController();
  final TextEditingController iduserController = TextEditingController();
  final TextEditingController cantidadrutasController = TextEditingController();
  final TextEditingController horastrabajadasController = TextEditingController();
  final TextEditingController observacionesController = TextEditingController();
  final TextEditingController fechaController = TextEditingController();

  void clear() {
    idController.clear();
    iduserController.clear();
    cantidadrutasController.clear();
    horastrabajadasController.clear();
    observacionesController.clear();
    fechaController.clear();
  }

  void dispose() {
    idController.dispose();
    iduserController.dispose();
    cantidadrutasController.dispose();
    horastrabajadasController.dispose();
    observacionesController.dispose();
    fechaController.dispose();
  }
}

// WIDGET PRINCIPAL
class BehaviorCrudWidget extends StatefulWidget {
  final String token;
  final VoidCallback? onSuccess;
  final VoidCallback? onBack;

  const BehaviorCrudWidget({
    Key? key,
    required this.token,
    this.onSuccess,
    this.onBack,
  }) : super(key: key);

  @override
  State<BehaviorCrudWidget> createState() => _BehaviorCrudWidgetState();
}

class _BehaviorCrudWidgetState extends State<BehaviorCrudWidget>
    with TickerProviderStateMixin, AutomaticKeepAliveClientMixin {
  late TabController _tabController;
  late BehaviorApiService _apiService;
  bool _isLoading = false;
  String? _message;
  MessageType? _messageType;

  List<BehaviorModel> _allBehaviors = [];
  List<BehaviorModel> _userBehaviors = [];

  final Map<String, BehaviorFormController> _formControllers = {};

  @override
  bool get wantKeepAlive => true;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 5, vsync: this);
    _apiService = BehaviorApiService(token: widget.token);
    _formControllers['create'] = BehaviorFormController();
    _formControllers['update'] = BehaviorFormController();
    _formControllers['delete'] = BehaviorFormController();
    _formControllers['findByUser'] = BehaviorFormController();
    _initializeData();
  }

  Future<void> _initializeData() async {
    await Future.wait([
      _loadNextId(),
      _loadAllBehaviors(),
    ]);
  }

  Future<void> _loadNextId() async {
    final response = await _apiService.getNextId();
    if (response.isSuccess && response.data != null) {
      _formControllers['create']?.idController.text = response.data.toString();
    }
  }

  Future<void> _createBehavior() async {
    final controller = _formControllers['create']!;
    if (!controller.formKey.currentState!.validate()) return;
    setState(() => _isLoading = true);
    final behavior = BehaviorModel(
      id: controller.idController.text.trim(),
      iduser: controller.iduserController.text.trim(),
      cantidadrutas: controller.cantidadrutasController.text.trim(),
      horastrabajadas: controller.horastrabajadasController.text.trim(),
      observaciones: controller.observacionesController.text.trim(),
      fecha: controller.fechaController.text.trim(),
    );
    final response = await _apiService.createBehavior(behavior);
    setState(() => _isLoading = false);
    if (response.isSuccess) {
      controller.clear();
      await Future.wait([_loadNextId(), _loadAllBehaviors()]);
    }
  }

  Future<void> _updateBehavior() async {
    final controller = _formControllers['update']!;
    if (!controller.formKey.currentState!.validate()) return;
    setState(() => _isLoading = true);
    final behavior = BehaviorModel(
      id: controller.idController.text.trim(),
      iduser: controller.iduserController.text.trim(),
      cantidadrutas: controller.cantidadrutasController.text.trim(),
      horastrabajadas: controller.horastrabajadasController.text.trim(),
      observaciones: controller.observacionesController.text.trim(),
      fecha: controller.fechaController.text.trim(),
    );
    final response = await _apiService.updateBehavior(behavior);
    setState(() => _isLoading = false);
    if (response.isSuccess) {
      await _loadAllBehaviors();
    }
  }

  Future<void> _deleteBehavior() async {
    final controller = _formControllers['delete']!;
    if (!controller.formKey.currentState!.validate()) return;
    final confirmed = await _showDeleteConfirmation();
    if (!confirmed) return;
    setState(() => _isLoading = true);
    final response = await _apiService.deleteBehavior(controller.idController.text.trim());
    setState(() => _isLoading = false);
    if (response.isSuccess) {
      controller.clear();
      await Future.wait([_loadNextId(), _loadAllBehaviors()]);
    }
  }

  Future<bool> _showDeleteConfirmation() async {
    return await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Confirmar eliminación'),
        content: const Text('¿Está seguro de que desea eliminar este rendimiento?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.of(context).pop(true),
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
            child: const Text('Eliminar'),
          ),
        ],
      ),
    ) ?? false;
  }

  Future<void> _loadAllBehaviors() async {
    setState(() => _isLoading = true);
    final response = await _apiService.getAllBehaviors();
    setState(() {
      _isLoading = false;
      if (response.isSuccess) {
        _allBehaviors = response.data ?? [];
      }
    });
  }

  Future<void> _findBehaviorsByUser() async {
    final controller = _formControllers['findByUser']!;
    if (!controller.formKey.currentState!.validate()) return;
    setState(() => _isLoading = true);
    final response = await _apiService.getBehaviorsByUser(controller.iduserController.text.trim());
    setState(() {
      _isLoading = false;
      if (response.isSuccess) {
        _userBehaviors = response.data ?? [];
      }
    });
  }

  Future<void> _selectDate(TextEditingController controller) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime(2020),
      lastDate: DateTime(2035),
    );
    if (picked != null) {
      controller.text = picked.toString().split(' ')[0];
    }
  }

  @override
  Widget build(BuildContext context) {
    super.build(context);
    return Scaffold(
      appBar: AppBar(
        title: const Text('Gestión de Rendimientos'),
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
        elevation: 2,
        leading: widget.onBack != null
            ? IconButton(
                icon: const Icon(Icons.arrow_back),
                onPressed: widget.onBack,
              )
            : null,
        bottom: TabBar(
          controller: _tabController,
          isScrollable: true,
          indicatorColor: Colors.white,
          labelColor: Colors.white,
          unselectedLabelColor: Colors.white70,
          tabs: const [
            Tab(icon: Icon(Icons.add), text: 'Crear'),
            Tab(icon: Icon(Icons.edit), text: 'Actualizar'),
            Tab(icon: Icon(Icons.delete), text: 'Eliminar'),
            Tab(icon: Icon(Icons.list), text: 'Todos'),
            Tab(icon: Icon(Icons.person_search), text: 'Por Usuario'),
          ],
        ),
      ),
      body: Column(
        children: [
          if (_message != null) _buildMessageBanner(),
          Expanded(
            child: TabBarView(
              controller: _tabController,
              children: [
                _buildFormTab('create', _createBehavior, 'Crear Rendimiento', Colors.blue, isCreate: true),
                _buildFormTab('update', _updateBehavior, 'Actualizar Rendimiento', Colors.purple),
                _buildDeleteTab(),
                _buildAllBehaviorsTab(),
                _buildBehaviorsByUserTab(),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMessageBanner() {
    final isError = _messageType == MessageType.error;
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      color: isError ? Colors.red[50] : Colors.green[50],
      child: Row(
        children: [
          Icon(
            isError ? Icons.error : Icons.check_circle,
            color: isError ? Colors.red[700] : Colors.green[700],
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              _message!,
              style: TextStyle(
                color: isError ? Colors.red[900] : Colors.green[900],
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.close),
            onPressed: () => setState(() {
              _message = null;
              _messageType = null;
            }),
          ),
        ],
      ),
    );
  }

  Widget _buildFormTab(String formKey, VoidCallback onSubmit, String buttonText, Color buttonColor, {bool isCreate = false}) {
    final controller = _formControllers[formKey]!;
    return Form(
      key: controller.formKey,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          CustomTextFormField(
            controller: controller.idController,
            label: 'ID',
            keyboardType: TextInputType.number,
            enabled: isCreate ? false : true, // Solo lectura en crear
            validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID' : null,
          ),
          const SizedBox(height: 16),
          CustomTextFormField(
            controller: controller.iduserController,
            label: 'Identificacion de Usuario',
            keyboardType: TextInputType.number,
            validator: (v) => v == null || v.isEmpty ? 'Ingrese el Identificacion del usuario' : null,
          ),
          const SizedBox(height: 16),
          CustomTextFormField(
            controller: controller.cantidadrutasController,
            label: 'Cantidad de Rutas',
            keyboardType: TextInputType.number,
            validator: (v) => v == null || v.isEmpty ? 'Ingrese la cantidad de rutas' : null,
          ),
          const SizedBox(height: 16),
          CustomTextFormField(
            controller: controller.horastrabajadasController,
            label: 'Horas Trabajadas',
            keyboardType: TextInputType.number,
            validator: (v) => v == null || v.isEmpty ? 'Ingrese las horas trabajadas' : null,
          ),
          const SizedBox(height: 16),
          CustomTextFormField(
            controller: controller.observacionesController,
            label: 'Observaciones',
            keyboardType: TextInputType.text,
            validator: (v) => v == null || v.isEmpty ? 'Ingrese observaciones' : null,
          ),
          const SizedBox(height: 16),
          CustomDateField(
            controller: controller.fechaController,
            label: 'Fecha',
            onTap: () => _selectDate(controller.fechaController),
            validator: (v) => v == null || v.isEmpty ? 'Seleccione la fecha' : null,
          ),
          const SizedBox(height: 32),
          CustomElevatedButton(
            onPressed: _isLoading ? null : onSubmit,
            backgroundColor: buttonColor,
            isLoading: _isLoading,
            child: Text(buttonText),
          ),
        ],
      ),
    );
  }

  Widget _buildDeleteTab() {
    final controller = _formControllers['delete']!;
    return Form(
      key: controller.formKey,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          CustomTextFormField(
            controller: controller.idController,
            label: 'ID a eliminar',
            keyboardType: TextInputType.number,
            validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID a eliminar' : null,
          ),
          const SizedBox(height: 32),
          CustomElevatedButton(
            onPressed: _isLoading ? null : _deleteBehavior,
            backgroundColor: Colors.red,
            isLoading: _isLoading,
            child: const Text('Eliminar Rendimiento'),
          ),
        ],
      ),
    );
  }

  Widget _buildAllBehaviorsTab() {
    if (_isLoading && _allBehaviors.isEmpty) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_allBehaviors.isEmpty) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.inbox, size: 64, color: Colors.grey),
            SizedBox(height: 16),
            Text('No hay rendimientos registrados', style: TextStyle(fontSize: 18, color: Colors.grey)),
          ],
        ),
      );
    }
    return RefreshIndicator(
      onRefresh: _loadAllBehaviors,
      child: ListView.builder(
        padding: const EdgeInsets.all(8),
        itemCount: _allBehaviors.length,
        itemBuilder: (context, index) {
          final beh = _allBehaviors[index];
          return BehaviorCard(behavior: beh);
        },
      ),
    );
  }

  Widget _buildBehaviorsByUserTab() {
    final controller = _formControllers['findByUser']!;
    return Form(
      key: controller.formKey,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          CustomTextFormField(
            controller: controller.iduserController,
            label: 'Identificacion de Usuario',
            keyboardType: TextInputType.number,
            validator: (v) => v == null || v.isEmpty ? 'Ingrese Identificacion de usuario' : null,
          ),
          const SizedBox(height: 16),
          CustomElevatedButton(
            onPressed: _isLoading ? null : _findBehaviorsByUser,
            backgroundColor: Colors.blue,
            isLoading: _isLoading,
            child: const Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(Icons.person_search),
                SizedBox(width: 8),
                Text('Buscar'),
              ],
            ),
          ),
          const SizedBox(height: 24),
          if (_userBehaviors.isEmpty && !_isLoading)
            const Text(
              'No hay rendimientos para ese usuario.',
              style: TextStyle(color: Colors.grey),
            ),
          ..._userBehaviors.map((behavior) => Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: BehaviorCard(behavior: behavior),
          )),
        ],
      ),
    );
  }
}

// WIDGETS PERSONALIZADOS
class BehaviorCard extends StatelessWidget {
  final BehaviorModel behavior;

  const BehaviorCard({Key? key, required this.behavior}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 2,
      margin: const EdgeInsets.symmetric(vertical: 4),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Text(
                  'ID: ${behavior.id ?? 'N/A'}',
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    color: Colors.grey,
                  ),
                ),
                const Spacer(),
                Text(
                  behavior.fecha ?? 'Sin fecha',
                  style: TextStyle(color: Colors.grey[700]),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text('Usuario: ${behavior.iduser ?? 'N/A'}'),
            Text('Cantidad de rutas: ${behavior.cantidadrutas ?? 'N/A'}'),
            Text('Horas trabajadas: ${behavior.horastrabajadas ?? 'N/A'}'),
            Text('Observaciones: ${behavior.observaciones ?? 'N/A'}'),
          ],
        ),
      ),
    );
  }
}
////Asistencia Widget Service
// MODELO
class AsistanceModel {
  final String? id;
  final String? iduser;
  final String? horainicio;
  final String? horafinal;
  final String? fecha;

  AsistanceModel({
    this.id,
    this.iduser,
    this.horainicio,
    this.horafinal,
    this.fecha,
  });

  factory AsistanceModel.fromJson(Map<String, dynamic> json) {
    return AsistanceModel(
      id: json['ID']?.toString(),
      iduser: json['iduser']?.toString(),
      horainicio: json['horainicio'],
      horafinal: json['horafinal'],
      fecha: json['fecha'],
    );
  }

  Map<String, String> toFormData() {
    return {
      if (id != null) 'id': id!,
      if (iduser != null) 'iduser': iduser!,
      if (horainicio != null) 'horainicio': horainicio!,
      if (horafinal != null) 'horafinal': horafinal!,
      if (fecha != null) 'fecha': fecha!,
    };
  }
}

// SERVICIO API
class AsistanceApiService {
  final String token;
  static const String _defaultBaseUrl = AppConfig.baseUrl;

  AsistanceApiService({required this.token});
  String get baseUrl => _defaultBaseUrl;

  Map<String, String> get _headers => {
    'Authorization': 'Bearer $token',
    'accept': 'application/json',
  };

  Map<String, String> get _formHeaders => {
    ..._headers,
    'Content-Type': 'application/x-www-form-urlencoded',
  };

  Future<ApiResponse<int>> getNextId() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/asistance/asistencias'),
        headers: _headers,
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final asistencias = (data['asistencias'] as List?) ?? [];
        int nextId = 1;
        if (asistencias.isNotEmpty) {
          final ids = asistencias.map((e) => int.tryParse(e['ID'].toString()) ?? 0).toList();
          nextId = (ids.isNotEmpty ? (ids.reduce((a, b) => a > b ? a : b)) : 0) + 1;
        }
        return ApiResponse.success(nextId);
      } else {
        return ApiResponse.error('No se pudo obtener el siguiente ID');
      }
    } catch (e) {
      return ApiResponse.error('Error de conexión al consultar el ID');
    }
  }

  Future<ApiResponse<String>> createAsistance(AsistanceModel asistance) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/asistance/create'),
        headers: _formHeaders,
        body: asistance.toFormData(),
      );
      if (response.statusCode == 201 || response.statusCode == 200) {
        return ApiResponse.success('Asistencia creada exitosamente');
      } else {
        return ApiResponse.error('No se pudo crear la asistencia: ${response.body}');
      }
    } catch (e) {
      return ApiResponse.error('Error de conexión al crear asistencia');
    }
  }

  Future<ApiResponse<String>> updateAsistance(AsistanceModel asistance) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/asistance/update'),
        headers: _formHeaders,
        body: asistance.toFormData(),
      );
      if (response.statusCode == 200) {
        return ApiResponse.success('Asistencia actualizada exitosamente');
      } else {
        return ApiResponse.error('No se pudo actualizar la asistencia: ${response.body}');
      }
    } catch (e) {
      return ApiResponse.error('Error de conexión al actualizar asistencia');
    }
  }

  Future<ApiResponse<String>> deleteAsistance(String id) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/asistance/delete'),
        headers: _formHeaders,
        body: {'id': id},
      );
      if (response.statusCode == 200) {
        return ApiResponse.success('Asistencia eliminada exitosamente');
      } else {
        return ApiResponse.error('No se pudo eliminar la asistencia: ${response.body}');
      }
    } catch (e) {
      return ApiResponse.error('Error de conexión al eliminar asistencia');
    }
  }

  Future<ApiResponse<List<AsistanceModel>>> getAllAsistances() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/asistance/asistencias'),
        headers: _headers,
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final asistencias = (data['asistencias'] as List?)
            ?.map((json) => AsistanceModel.fromJson(json))
            .toList() ?? [];
        return ApiResponse.success(asistencias);
      } else {
        return ApiResponse.error('Error al cargar asistencias: ${response.body}');
      }
    } catch (e) {
      return ApiResponse.error('Error de conexión al cargar asistencias');
    }
  }

  Future<ApiResponse<List<AsistanceModel>>> getAsistancesByUser(String iduser) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/asistance/user?iduser=$iduser'),
        headers: _headers,
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final asistencias = (data['asistencias'] as List?)
            ?.map((json) => AsistanceModel.fromJson(json))
            .toList() ?? [];
        return ApiResponse.success(asistencias);
      } else {
        return ApiResponse.error('No se encontraron asistencias para ese usuario');
      }
    } catch (e) {
      return ApiResponse.error('Error de conexión al buscar asistencias del usuario');
    }
  }
}

// CONTROLADOR DE FORMULARIO
class AsistanceFormController {
  final GlobalKey<FormState> formKey = GlobalKey<FormState>();
  final TextEditingController idController = TextEditingController();
  final TextEditingController iduserController = TextEditingController();
  final TextEditingController horainicioController = TextEditingController();
  final TextEditingController horafinalController = TextEditingController();
  final TextEditingController fechaController = TextEditingController();

  void clear() {
    idController.clear();
    iduserController.clear();
    horainicioController.clear();
    horafinalController.clear();
    fechaController.clear();
  }

  void dispose() {
    idController.dispose();
    iduserController.dispose();
    horainicioController.dispose();
    horafinalController.dispose();
    fechaController.dispose();
  }
}

// WIDGET PRINCIPAL
class AsistanceCrudWidget extends StatefulWidget {
  final String token;
  final VoidCallback? onSuccess;
  final VoidCallback? onBack;

  const AsistanceCrudWidget({
    Key? key,
    required this.token,
    this.onSuccess,
    this.onBack,
  }) : super(key: key);

  @override
  State<AsistanceCrudWidget> createState() => _AsistanceCrudWidgetState();
}

class _AsistanceCrudWidgetState extends State<AsistanceCrudWidget>
    with TickerProviderStateMixin, AutomaticKeepAliveClientMixin {
  late TabController _tabController;
  late AsistanceApiService _apiService;
  bool _isLoading = false;
  String? _message;
  MessageType? _messageType;

  List<AsistanceModel> _allAsistances = [];
  List<AsistanceModel> _userAsistances = [];

  final Map<String, AsistanceFormController> _formControllers = {};

  @override
  bool get wantKeepAlive => true;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 5, vsync: this);
    _apiService = AsistanceApiService(token: widget.token);
    _formControllers['create'] = AsistanceFormController();
    _formControllers['update'] = AsistanceFormController();
    _formControllers['delete'] = AsistanceFormController();
    _formControllers['findByUser'] = AsistanceFormController();
    _initializeData();
  }

  Future<void> _initializeData() async {
    await Future.wait([
      _loadNextId(),
      _loadAllAsistances(),
    ]);
  }

  Future<void> _loadNextId() async {
    final response = await _apiService.getNextId();
    if (response.isSuccess && response.data != null) {
      _formControllers['create']?.idController.text = response.data.toString();
    }
  }

  Future<void> _createAsistance() async {
    final controller = _formControllers['create']!;
    if (!controller.formKey.currentState!.validate()) return;
    setState(() => _isLoading = true);
    final asistance = AsistanceModel(
      id: controller.idController.text.trim(),
      iduser: controller.iduserController.text.trim(),
      horainicio: controller.horainicioController.text.trim(),
      horafinal: controller.horafinalController.text.trim(),
      fecha: controller.fechaController.text.trim(),
    );
    final response = await _apiService.createAsistance(asistance);
    setState(() => _isLoading = false);
    if (response.isSuccess) {
      controller.clear();
      await Future.wait([_loadNextId(), _loadAllAsistances()]);
      widget.onSuccess?.call();
    }
  }

  Future<void> _updateAsistance() async {
    final controller = _formControllers['update']!;
    if (!controller.formKey.currentState!.validate()) return;
    setState(() => _isLoading = true);
    final asistance = AsistanceModel(
      id: controller.idController.text.trim(),
      iduser: controller.iduserController.text.trim(),
      horainicio: controller.horainicioController.text.trim(),
      horafinal: controller.horafinalController.text.trim(),
      fecha: controller.fechaController.text.trim(),
    );
    final response = await _apiService.updateAsistance(asistance);
    setState(() => _isLoading = false);
    if (response.isSuccess) {
      await _loadAllAsistances();
    }
  }

  Future<void> _deleteAsistance() async {
    final controller = _formControllers['delete']!;
    if (!controller.formKey.currentState!.validate()) return;
    final confirmed = await _showDeleteConfirmation();
    if (!confirmed) return;
    setState(() => _isLoading = true);
    final response = await _apiService.deleteAsistance(controller.idController.text.trim());
    setState(() => _isLoading = false);
    if (response.isSuccess) {
      controller.clear();
      await Future.wait([_loadNextId(), _loadAllAsistances()]);
    }
  }

  Future<bool> _showDeleteConfirmation() async {
    return await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Confirmar eliminación'),
        content: const Text('¿Está seguro de que desea eliminar esta asistencia?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.of(context).pop(true),
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
            child: const Text('Eliminar'),
          ),
        ],
      ),
    ) ?? false;
  }

  Future<void> _loadAllAsistances() async {
    setState(() => _isLoading = true);
    final response = await _apiService.getAllAsistances();
    setState(() {
      _isLoading = false;
      if (response.isSuccess) {
        _allAsistances = response.data ?? [];
      }
    });
  }

  Future<void> _findAsistancesByUser() async {
    final controller = _formControllers['findByUser']!;
    if (!controller.formKey.currentState!.validate()) return;
    setState(() => _isLoading = true);
    final response = await _apiService.getAsistancesByUser(controller.iduserController.text.trim());
    setState(() {
      _isLoading = false;
      if (response.isSuccess) {
        _userAsistances = response.data ?? [];
      }
    });
  }

  Future<void> _selectTime(TextEditingController controller) async {
    final TimeOfDay? picked = await showTimePicker(
      context: context,
      initialTime: TimeOfDay.now(),
    );
    if (picked != null) {
      controller.text = picked.format(context);
    }
  }

  Future<void> _selectDate(TextEditingController controller) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime(2020),
      lastDate: DateTime(2030),
    );
    if (picked != null) {
      controller.text = picked.toString().split(' ')[0];
    }
  }

  @override
  Widget build(BuildContext context) {
    super.build(context);
    return Scaffold(
      appBar: AppBar(
        title: const Text('Gestión de Asistencias'),
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
        elevation: 2,
        leading: widget.onBack != null
            ? IconButton(
                icon: const Icon(Icons.arrow_back),
                onPressed: widget.onBack,
              )
            : null,
        bottom: TabBar(
          controller: _tabController,
          isScrollable: true,
          indicatorColor: Colors.white,
          labelColor: Colors.white,
          unselectedLabelColor: Colors.white70,
          tabs: const [
            Tab(icon: Icon(Icons.add), text: 'Crear'),
            Tab(icon: Icon(Icons.edit), text: 'Actualizar'),
            Tab(icon: Icon(Icons.delete), text: 'Eliminar'),
            Tab(icon: Icon(Icons.list), text: 'Todas'),
            Tab(icon: Icon(Icons.person_search), text: 'Por Usuario'),
          ],
        ),
      ),
      body: Column(
        children: [
          if (_message != null) _buildMessageBanner(),
          Expanded(
            child: TabBarView(
              controller: _tabController,
              children: [
                _buildFormTab('create', _createAsistance, 'Crear Asistencia', Colors.blue, isCreate: true),
                _buildFormTab('update', _updateAsistance, 'Actualizar Asistencia', Colors.purple),
                _buildDeleteTab(),
                _buildAllAsistancesTab(),
                _buildAllAsistancesByUserIDTab(),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMessageBanner() {
    final isError = _messageType == MessageType.error;
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      color: isError ? Colors.red[50] : Colors.green[50],
      child: Row(
        children: [
          Icon(
            isError ? Icons.error : Icons.check_circle,
            color: isError ? Colors.red[700] : Colors.green[700],
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              _message!,
              style: TextStyle(
                color: isError ? Colors.red[900] : Colors.green[900],
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.close),
            onPressed: () => setState(() {
              _message = null;
              _messageType = null;
            }),
          ),
        ],
      ),
    );
  }

  Widget _buildFormTab(String formKey, VoidCallback onSubmit, String buttonText, Color buttonColor, {bool isCreate = false}) {
    final controller = _formControllers[formKey]!;
    return Form(
      key: controller.formKey,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          CustomTextFormField(
            controller: controller.idController,
            label: 'ID',
            keyboardType: TextInputType.number,
            enabled: isCreate ? false : true, // Solo lectura en crear
            validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID' : null,
          ),
          const SizedBox(height: 16),
          CustomTextFormField(
            controller: controller.iduserController,
            label: 'ID Usuario',
            keyboardType: TextInputType.number,
            validator: (v) => v == null || v.isEmpty ? 'Ingrese el número de Identificación del usuario' : null,
          ),
          const SizedBox(height: 16),
          CustomTimeField(
            controller: controller.horainicioController,
            label: 'Hora Inicio',
            onTap: () => _selectTime(controller.horainicioController),
            validator: (v) => v == null || v.isEmpty ? 'Seleccione la hora de inicio' : null,
          ),
          const SizedBox(height: 16),
          CustomTimeField(
            controller: controller.horafinalController,
            label: 'Hora Final',
            onTap: () => _selectTime(controller.horafinalController),
            validator: (v) => v == null || v.isEmpty ? 'Seleccione la hora de finalización' : null,
          ),
          const SizedBox(height: 16),
          CustomDateField(
            controller: controller.fechaController,
            label: 'Fecha',
            onTap: () => _selectDate(controller.fechaController),
            validator: (v) => v == null || v.isEmpty ? 'Seleccione la fecha' : null,
          ),
          const SizedBox(height: 32),
          CustomElevatedButton(
            onPressed: _isLoading ? null : onSubmit,
            backgroundColor: buttonColor,
            isLoading: _isLoading,
            child: Text(buttonText),
          ),
        ],
      ),
    );
  }

  Widget _buildDeleteTab() {
    final controller = _formControllers['delete']!;
    return Form(
      key: controller.formKey,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          CustomTextFormField(
            controller: controller.idController,
            label: 'ID a eliminar',
            keyboardType: TextInputType.number,
            validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID a eliminar' : null,
          ),
          const SizedBox(height: 32),
          CustomElevatedButton(
            onPressed: _isLoading ? null : _deleteAsistance,
            backgroundColor: Colors.red,
            isLoading: _isLoading,
            child: const Text('Eliminar Asistencia'),
          ),
        ],
      ),
    );
  }

  Widget _buildAllAsistancesTab() {
    if (_isLoading && _allAsistances.isEmpty) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_allAsistances.isEmpty) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.inbox, size: 64, color: Colors.grey),
            SizedBox(height: 16),
            Text('No hay asistencias registradas', style: TextStyle(fontSize: 18, color: Colors.grey)),
          ],
        ),
      );
    }
    return RefreshIndicator(
      onRefresh: _loadAllAsistances,
      child: ListView.builder(
        padding: const EdgeInsets.all(8),
        itemCount: _allAsistances.length,
        itemBuilder: (context, index) {
          final asis = _allAsistances[index];
          return AsistanceCard(asistance: asis);
        },
      ),
    );
  }

  Widget _buildAllAsistancesByUserIDTab() {
    final controller = _formControllers['findByUser']!;
    return Form(
      key: controller.formKey,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          CustomTextFormField(
            controller: controller.iduserController,
            label: 'ID Usuario',
            keyboardType: TextInputType.number,
            validator: (v) => v == null || v.isEmpty ? 'Ingrese el número de Identificación de usuario' : null,
          ),
          const SizedBox(height: 16),
          CustomElevatedButton(
            onPressed: _isLoading ? null : _findAsistancesByUser,
            backgroundColor: Colors.blue,
            isLoading: _isLoading,
            child: const Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(Icons.person_search),
                SizedBox(width: 8),
                Text('Buscar'),
              ],
            ),
          ),
          const SizedBox(height: 24),
          if (_userAsistances.isEmpty && !_isLoading)
            const Text(
              'No hay asistencias para ese usuario.',
              style: TextStyle(color: Colors.grey),
            ),
          ..._userAsistances.map((asistencia) => Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: AsistanceCard(asistance: asistencia),
          )),
        ],
      ),
    );
  }
}

// WIDGETS PERSONALIZADOS

class CustomTimeField extends StatelessWidget {
  final TextEditingController controller;
  final String label;
  final VoidCallback onTap;
  final String? Function(String?)? validator;

  const CustomTimeField({
    Key? key,
    required this.controller,
    required this.label,
    required this.onTap,
    this.validator,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      controller: controller,
      readOnly: true,
      decoration: InputDecoration(
        labelText: label,
        border: const OutlineInputBorder(),
        suffixIcon: const Icon(Icons.access_time),
      ),
      onTap: onTap,
      validator: validator,
    );
  }
}

class AsistanceCard extends StatelessWidget {
  final AsistanceModel asistance;

  const AsistanceCard({Key? key, required this.asistance}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 2,
      margin: const EdgeInsets.symmetric(vertical: 4),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Text(
                  'ID: ${asistance.id ?? 'N/A'}',
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    color: Colors.grey,
                  ),
                ),
                const Spacer(),
                Text(
                  asistance.fecha ?? 'Sin fecha',
                  style: TextStyle(color: Colors.grey[700]),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                Icon(Icons.person, size: 16, color: Colors.grey[600]),
                const SizedBox(width: 4),
                Text(
                  'Usuario: ${asistance.iduser ?? 'N/A'}',
                  style: TextStyle(color: Colors.grey[600]),
                ),
                const Spacer(),
                Icon(Icons.access_time, size: 16, color: Colors.grey[600]),
                const SizedBox(width: 4),
                Text(
                  '${asistance.horainicio ?? ''} - ${asistance.horafinal ?? ''}',
                  style: TextStyle(color: Colors.grey[600]),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
///
///PRICE CUD SERVICE
//CREATE
// MODELO
class PriceModel {
  final int id;
  final int idTipoTransporte;
  final double monto;

  PriceModel({
    required this.id,
    required this.idTipoTransporte,
    required this.monto,
  });

  Map<String, String> toFormData() {
    return {
      "ID": id.toString(),
      "IDTipoTransporte": idTipoTransporte.toString(),
      "Monto": monto.toString(),
    };
  }
}

// SERVICIO API
class PriceApiService {
  final String baseUrl;
  final String token;

  PriceApiService({required this.baseUrl, required this.token});

  Future<ApiResponse<String>> createPrice(PriceModel price) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/create'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json',
        },
        body: price.toFormData(),
      );
      if (response.statusCode == 201) {
        final data = json.decode(response.body);
        return ApiResponse.success(data["message"] ?? "Creado correctamente");
      } else {
        final data = json.decode(response.body);
        return ApiResponse.error(data["detail"] ?? "Error al crear tarifa");
      }
    } catch (e) {
      return ApiResponse.error("Error de conexión: $e");
    }
  }
}

// WIDGET
class PriceCreateWidget extends StatefulWidget {
  final String baseUrl;
  final String token;
  final VoidCallback? onSuccess;
  final VoidCallback? onBack;
  const PriceCreateWidget({Key? key, 
    required this.baseUrl,
    required this.token,
    this.onSuccess,
    this.onBack,
    }) : super(key: key);

  @override
  State<PriceCreateWidget> createState() => _PriceCreateWidgetState();
}

class _PriceCreateWidgetState extends State<PriceCreateWidget> {
  final _formKey = GlobalKey<FormState>();
  final _idController = TextEditingController();
  final _idTipoTransporteController = TextEditingController();
  final _montoController = TextEditingController();

  bool _isLoading = false;
  String? _message;
  bool _isSuccess = false;

  late PriceApiService _apiService;

  @override
  void initState() {
    super.initState();
    _apiService = PriceApiService(baseUrl: widget.baseUrl, token: widget.token);
  }

  @override
  void dispose() {
    _idController.dispose();
    _idTipoTransporteController.dispose();
    _montoController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _isLoading = true;
      _message = null;
    });

    final price = PriceModel(
      id: int.parse(_idController.text),
      idTipoTransporte: int.parse(_idTipoTransporteController.text),
      monto: double.parse(_montoController.text),
    );

    final response = await _apiService.createPrice(price);
    setState(() {
      _isLoading = false;
      _message = response.isSuccess ? response.data : response.error;
      _isSuccess = response.isSuccess;
      if (response.isSuccess) {
        _formKey.currentState?.reset();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Crear Tarifa')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: ListView(
            children: [
              if (_message != null)
                Container(
                  margin: const EdgeInsets.only(bottom: 20),
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: _isSuccess ? Colors.green[100] : Colors.red[100],
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Text(
                    _message!,
                    style: TextStyle(
                      color: _isSuccess ? Colors.green[800] : Colors.red[800],
                    ),
                  ),
                ),
              TextFormField(
                controller: _idController,
                decoration: const InputDecoration(
                  labelText: 'ID',
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.number,
                validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID' : null,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _idTipoTransporteController,
                decoration: const InputDecoration(
                  labelText: 'ID Tipo Transporte',
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.number,
                validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID de Tipo de Transporte' : null,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _montoController,
                decoration: const InputDecoration(
                  labelText: 'Monto',
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.numberWithOptions(decimal: true),
                validator: (v) {
                  if (v == null || v.isEmpty) return 'Ingrese el monto';
                  final val = double.tryParse(v);
                  if (val == null || val <= 0) return 'Monto no válido';
                  return null;
                },
              ),
              const SizedBox(height: 32),
              SizedBox(
                width: double.infinity,
                height: 48,
                child: ElevatedButton(
                  onPressed: _isLoading ? null : _submit,
                  child: _isLoading
                      ? const CircularProgressIndicator(color: Colors.white)
                      : const Text('Crear Tarifa'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}class RutaParadaCrudWidget extends StatefulWidget {
  final String token;
  const RutaParadaCrudWidget({Key? key, required this.token}) : super(key: key);

  @override
  State<RutaParadaCrudWidget> createState() => _RutaParadaCrudWidgetState();
}

class _RutaParadaCrudWidgetState extends State<RutaParadaCrudWidget> {
  bool _loading = true;
  String? _error;
  List<dynamic> _relaciones = [];

  final _formKey = GlobalKey<FormState>();
  final _idRutaController = TextEditingController();
  final _idParadaController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _fetch();
  }

  Future<void> _fetch() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/ruta_parada/solo_nombres'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
        },
      );
      if (response.statusCode == 200) {
        setState(() {
          _relaciones = json.decode(response.body);
        });
      } else {
        setState(() {
          _error = 'No se pudo obtener la lista. (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión.';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  Future<void> _crear() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _loading = true);
    try {
      final response = await http.post(
        Uri.parse('${AppConfig.baseUrl}/rutaparada/create'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: {
          'IDRuta': _idRutaController.text.trim(),
          'IDParada': _idParadaController.text.trim(),
        },
      );
      if (response.statusCode == 200 || response.statusCode == 201) {
        _idRutaController.clear();
        _idParadaController.clear();
        await _fetch();
      } else {
        setState(() {
          _error = 'No se pudo crear la relación. (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión.';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  Future<void> _eliminar(Map<String, dynamic> rel) async {
    setState(() => _loading = true);
    try {
      final response = await http.post(
        Uri.parse('${AppConfig.baseUrl}/rutaparada/delete'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: {
          'IDRuta': rel['IDRuta'].toString(),
          'IDParada': rel['IDParada'].toString(),
        },
      );
      if (response.statusCode == 200) {
        await _fetch();
      } else {
        setState(() {
          _error = 'No se pudo eliminar la relación. (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión.';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text('Gestión Ruta-Parada', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20)),
          const SizedBox(height: 16),
          Form(
            key: _formKey,
            child: Row(
              children: [
                Expanded(
                  child: TextFormField(
                    controller: _idRutaController,
                    decoration: InputDecoration(labelText: 'ID Ruta'),
                    validator: (v) => v == null || v.isEmpty ? 'Ingrese ID Ruta' : null,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: TextFormField(
                    controller: _idParadaController,
                    decoration: InputDecoration(labelText: 'ID Parada'),
                    validator: (v) => v == null || v.isEmpty ? 'Ingrese ID Parada' : null,
                  ),
                ),
                const SizedBox(width: 12),
                ElevatedButton(
                  onPressed: _loading ? null : _crear,
                  child: _loading ? SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white)) : Text('Crear'),
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),
          if (_loading)
            Center(child: CircularProgressIndicator())
          else if (_error != null)
            Text(_error!, style: TextStyle(color: Colors.red))
          else
            Expanded(
              child: ListView.separated(
                shrinkWrap: true,
                itemCount: _relaciones.length,
                separatorBuilder: (_, __) => Divider(),
                itemBuilder: (context, i) {
                  final rel = _relaciones[i];
                  return ListTile(
                    title: Text('Ruta: ${rel['NombreRuta'] ?? '-'}'),
                    subtitle: Text('Parada: ${rel['NombreParada'] ?? '-'}'),
                    trailing: IconButton(
                      icon: Icon(Icons.delete, color: Colors.red),
                      onPressed: _loading ? null : () => _eliminar(rel),
                    ),
                  );
                },
              ),
            ),
        ],
      ),
    );
  }
}
/// Rol User Widget
class RolUser {
  final int id;
  final String rol;
  
  RolUser({required this.id, required this.rol});
  
  factory RolUser.fromJson(Map<String, dynamic> json) =>
      RolUser(id: json['ID'], rol: json['Rol']);
      
  Map<String, dynamic> toJson() => {
    'ID': id,
    'Rol': rol,
  };
}

class RolUserCrudTabsWidget extends StatefulWidget {
  final String token;
  final VoidCallback onSuccess;

  const RolUserCrudTabsWidget({
    Key? key,
    required this.token,
    required this.onSuccess,
  }) : super(key: key);

  @override
  State<RolUserCrudTabsWidget> createState() => _RolUserCrudTabsWidgetState();
}

class _RolUserCrudTabsWidgetState extends State<RolUserCrudTabsWidget>
    with SingleTickerProviderStateMixin {
  final _formKey = GlobalKey<FormState>();
  final _idController = TextEditingController();
  final _rolController = TextEditingController();
  
  String? _output;
  List<RolUser> _rolUsers = [];
  bool _isLoading = false;
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 4, vsync: this);
    _consultar(); // Load data on init
  }

  @override
  void dispose() {
    _idController.dispose();
    _rolController.dispose();
    _tabController.dispose();
    super.dispose();
  }

  void _setLoading(bool loading) {
    setState(() {
      _isLoading = loading;
    });
  }

  void _showMessage(String message, {bool isError = false}) {
    setState(() {
      _output = message;
    });
    
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: isError ? Colors.red : Colors.green,
        duration: Duration(seconds: 3),
      ),
    );
  }

  void _clearForm() {
    _idController.clear();
    _rolController.clear();
    setState(() {
      _output = null;
    });
  }

  Future<void> _agregar() async {
    if (!_formKey.currentState!.validate()) return;
    
    final rolText = _rolController.text.trim();
    if (rolText.isEmpty) {
      _showMessage("El campo Rol es requerido", isError: true);
      return;
    }

    _setLoading(true);
    
    try {
      // Get next available ID
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/roluser/administrador/rolusers'),
        headers: {'Authorization': 'Bearer ${widget.token}'},
      );
      
      int nextId = 1;
      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body)['rolusers'];
        if (data.isNotEmpty) {
          nextId = data.map((e) => e['ID'] as int).reduce((a, b) => a > b ? a : b) + 1;
        }
      } else {
        _showMessage("Error al consultar roles: ${response.body}", isError: true);
        return;
      }

      // Create new role
      final createResponse = await http.post(
        Uri.parse('${AppConfig.baseUrl}/roluser/create'),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Authorization': 'Bearer ${widget.token}',
        },
        body: {
          'ID': nextId.toString(),
          'Rol': rolText,
        },
      );

      if (createResponse.statusCode == 201 || createResponse.statusCode == 200) {
        _showMessage("Rol creado exitosamente");
        await _consultar(); // Refresh the list
      } else {
        _showMessage("Error al crear rol: ${createResponse.body}", isError: true);
      }
    } catch (e) {
      _showMessage("Error de conexión: $e", isError: true);
    } finally {
      _setLoading(false);
    }
  }

  Future<void> _actualizar() async {
    if (!_formKey.currentState!.validate()) return;
    
    final idText = _idController.text.trim();
    final rolText = _rolController.text.trim();
    
    if (idText.isEmpty || rolText.isEmpty) {
      _showMessage("Todos los campos son requeridos", isError: true);
      return;
    }

    _setLoading(true);
    
    try {
      final response = await http.post(
        Uri.parse('${AppConfig.baseUrl}/roluser/update'),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Authorization': 'Bearer ${widget.token}',
        },
        body: {
          'ID': idText,
          'Rol': rolText,
        },
      );

      if (response.statusCode == 200) {
        _showMessage("Rol actualizado exitosamente");
        await _consultar(); // Refresh the list
      } else {
        _showMessage("Error al actualizar rol: ${response.body}", isError: true);
      }
    } catch (e) {
      _showMessage("Error de conexión: $e", isError: true);
    } finally {
      _setLoading(false);
    }
  }

  Future<void> _eliminar() async {
    final idText = _idController.text.trim();
    
    if (idText.isEmpty) {
      _showMessage("El campo ID es requerido", isError: true);
      return;
    }

    // Show confirmation dialog
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text("Confirmar eliminación"),
        content: Text("¿Está seguro de que desea eliminar el rol con ID $idText?"),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: Text("Cancelar"),
          ),
          TextButton(
            onPressed: () => Navigator.of(context).pop(true),
            style: TextButton.styleFrom(foregroundColor: Colors.red),
            child: Text("Eliminar"),
          ),
        ],
      ),
    );

    if (confirmed != true) return;

    _setLoading(true);
    
    try {
      final response = await http.post(
        Uri.parse('${AppConfig.baseUrl}/roluser/delete'),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Authorization': 'Bearer ${widget.token}',
        },
        body: {
          'ID': idText,
        },
      );

      if (response.statusCode == 200) {
        _showMessage("Rol eliminado exitosamente");
        await _consultar(); // Refresh the list
      } else {
        _showMessage("Error al eliminar rol: ${response.body}", isError: true);
      }
    } catch (e) {
      _showMessage("Error de conexión: $e", isError: true);
    } finally {
      _setLoading(false);
    }
  }

  Future<void> _consultar() async {
    _setLoading(true);
    
    try {
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/roluser/administrador/rolusers'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
        },
      );
      
      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body)['rolusers'];
        setState(() {
          _rolUsers = data.map((e) => RolUser.fromJson(e)).toList();
          _output = null;
        });
      } else {
        _showMessage("Error al consultar roles: ${response.body}", isError: true);
      }
    } catch (e) {
      _showMessage("Error de conexión: $e", isError: true);
    } finally {
      _setLoading(false);
    }
  }

  void _selectRolFromList(RolUser rolUser) {
    setState(() {
      _idController.text = rolUser.id.toString();
      _rolController.text = rolUser.rol;
    });
    _tabController.animateTo(1); // Switch to update tab
  }

  Widget _buildLoadingOverlay({required Widget child}) {
    return Stack(
      children: [
        child,
        if (_isLoading)
          Container(
            color: Colors.black26,
            child: Center(
              child: CircularProgressIndicator(),
            ),
          ),
      ],
    );
  }

  Widget _buildFormField({
    required TextEditingController controller,
    required String label,
    TextInputType? keyboardType,
    String? Function(String?)? validator,
  }) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: TextFormField(
        controller: controller,
        decoration: InputDecoration(
          labelText: label,
          border: OutlineInputBorder(),
          contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        ),
        keyboardType: keyboardType,
        validator: validator,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 4,
      child: Column(
        children: [
          Container(
            decoration: BoxDecoration(
              color: Theme.of(context).cardColor,
              boxShadow: [
                BoxShadow(
                  color: Colors.black12,
                  blurRadius: 4,
                  offset: Offset(0, 2),
                ),
              ],
            ),
            child: TabBar(
              controller: _tabController,
              labelColor: Theme.of(context).primaryColor,
              unselectedLabelColor: Colors.grey,
              indicatorColor: Theme.of(context).primaryColor,
              tabs: [
                Tab(icon: Icon(Icons.add), text: "Agregar"),
                Tab(icon: Icon(Icons.edit), text: "Actualizar"),
                Tab(icon: Icon(Icons.delete), text: "Eliminar"),
                Tab(icon: Icon(Icons.list), text: "Consultar"),
              ],
            ),
          ),
          Expanded(
            child: _buildLoadingOverlay(
              child: TabBarView(
                controller: _tabController,
                children: [
                  // AGREGAR TAB
                  SingleChildScrollView(
                    padding: const EdgeInsets.all(16),
                    child: Form(
                      key: _formKey,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          Text(
                            "Crear Nuevo Rol",
                            style: Theme.of(context).textTheme.headlineSmall,
                          ),
                          SizedBox(height: 16),
                          _buildFormField(
                            controller: _rolController,
                            label: "Nombre del Rol",
                            validator: (value) {
                              if (value == null || value.trim().isEmpty) {
                                return "Este campo es requerido";
                              }
                              if (value.trim().length < 2) {
                                return "El rol debe tener al menos 2 caracteres";
                              }
                              return null;
                            },
                          ),
                          SizedBox(height: 24),
                          ElevatedButton.icon(
                            onPressed: _isLoading ? null : _agregar,
                            icon: Icon(Icons.add),
                            label: Text("Crear Rol"),
                            style: ElevatedButton.styleFrom(
                              padding: EdgeInsets.symmetric(vertical: 16),
                            ),
                          ),
                          if (_output != null) ...[
                            SizedBox(height: 16),
                            Container(
                              padding: EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: Colors.grey[100],
                                borderRadius: BorderRadius.circular(8),
                              ),
                              child: Text(
                                "Respuesta:\n$_output",
                                style: TextStyle(fontFamily: 'monospace'),
                              ),
                            ),
                          ],
                        ],
                      ),
                    ),
                  ),
                  
                  // ACTUALIZAR TAB
                  SingleChildScrollView(
                    padding: const EdgeInsets.all(16),
                    child: Form(
                      key: _formKey,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          Text(
                            "Actualizar Rol",
                            style: Theme.of(context).textTheme.headlineSmall,
                          ),
                          SizedBox(height: 16),
                          _buildFormField(
                            controller: _idController,
                            label: "ID del Rol",
                            keyboardType: TextInputType.number,
                            validator: (value) {
                              if (value == null || value.trim().isEmpty) {
                                return "Este campo es requerido";
                              }
                              if (int.tryParse(value.trim()) == null) {
                                return "Debe ser un número válido";
                              }
                              return null;
                            },
                          ),
                          _buildFormField(
                            controller: _rolController,
                            label: "Nuevo Nombre del Rol",
                            validator: (value) {
                              if (value == null || value.trim().isEmpty) {
                                return "Este campo es requerido";
                              }
                              if (value.trim().length < 2) {
                                return "El rol debe tener al menos 2 caracteres";
                              }
                              return null;
                            },
                          ),
                          SizedBox(height: 24),
                          ElevatedButton.icon(
                            onPressed: _isLoading ? null : _actualizar,
                            icon: Icon(Icons.update),
                            label: Text("Actualizar Rol"),
                            style: ElevatedButton.styleFrom(
                              padding: EdgeInsets.symmetric(vertical: 16),
                            ),
                          ),
                          if (_output != null) ...[
                            SizedBox(height: 16),
                            Container(
                              padding: EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: Colors.grey[100],
                                borderRadius: BorderRadius.circular(8),
                              ),
                              child: Text(
                                "Respuesta:\n$_output",
                                style: TextStyle(fontFamily: 'monospace'),
                              ),
                            ),
                          ],
                        ],
                      ),
                    ),
                  ),
                  
                  // ELIMINAR TAB
                  SingleChildScrollView(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Text(
                          "Eliminar Rol",
                          style: Theme.of(context).textTheme.headlineSmall,
                        ),
                        SizedBox(height: 16),
                        Container(
                          padding: EdgeInsets.all(12),
                          decoration: BoxDecoration(
                            color: Colors.red[50],
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(color: Colors.red[200]!),
                          ),
                          child: Row(
                            children: [
                              Icon(Icons.warning, color: Colors.red),
                              SizedBox(width: 8),
                              Expanded(
                                child: Text(
                                  "Esta acción no se puede deshacer",
                                  style: TextStyle(color: Colors.red[700]),
                                ),
                              ),
                            ],
                          ),
                        ),
                        SizedBox(height: 16),
                        _buildFormField(
                          controller: _idController,
                          label: "ID del Rol a Eliminar",
                          keyboardType: TextInputType.number,
                        ),
                        SizedBox(height: 24),
                        ElevatedButton.icon(
                          onPressed: _isLoading ? null : _eliminar,
                          icon: Icon(Icons.delete),
                          label: Text("Eliminar Rol"),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.red,
                            foregroundColor: Colors.white,
                            padding: EdgeInsets.symmetric(vertical: 16),
                          ),
                        ),
                        if (_output != null) ...[
                          SizedBox(height: 16),
                          Container(
                            padding: EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: Colors.grey[100],
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: Text(
                              "Respuesta:\n$_output",
                              style: TextStyle(fontFamily: 'monospace'),
                            ),
                          ),
                        ],
                      ],
                    ),
                  ),
                  
                  // CONSULTAR TAB
                  Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              "Lista de Roles",
                              style: Theme.of(context).textTheme.headlineSmall,
                            ),
                            IconButton(
                              onPressed: _isLoading ? null : _consultar,
                              icon: Icon(Icons.refresh),
                              tooltip: "Actualizar lista",
                            ),
                          ],
                        ),
                        SizedBox(height: 16),
                        Expanded(
                          child: _rolUsers.isEmpty
                              ? Center(
                                  child: Column(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      Icon(
                                        Icons.inbox,
                                        size: 64,
                                        color: Colors.grey,
                                      ),
                                      SizedBox(height: 16),
                                      Text(
                                        "No hay roles para mostrar",
                                        style: TextStyle(
                                          fontSize: 16,
                                          color: Colors.grey[600],
                                        ),
                                      ),
                                      SizedBox(height: 8),
                                      TextButton.icon(
                                        onPressed: _consultar,
                                        icon: Icon(Icons.refresh),
                                        label: Text("Recargar"),
                                      ),
                                    ],
                                  ),
                                )
                              : ListView.builder(
                                  itemCount: _rolUsers.length,
                                  itemBuilder: (context, index) {
                                    final rolUser = _rolUsers[index];
                                    return Card(
                                      margin: EdgeInsets.symmetric(vertical: 4),
                                      child: ListTile(
                                        leading: CircleAvatar(
                                          child: Text('${rolUser.id}'),
                                          backgroundColor: Theme.of(context).primaryColor,
                                          foregroundColor: Colors.white,
                                        ),
                                        title: Text(
                                          rolUser.rol,
                                          style: TextStyle(fontWeight: FontWeight.w500),
                                        ),
                                        subtitle: Text('ID: ${rolUser.id}'),
                                        trailing: PopupMenuButton(
                                          itemBuilder: (context) => [
                                            PopupMenuItem(
                                              value: 'edit',
                                              child: Row(
                                                children: [
                                                  Icon(Icons.edit, size: 16),
                                                  SizedBox(width: 8),
                                                  Text('Editar'),
                                                ],
                                              ),
                                            ),
                                            PopupMenuItem(
                                              value: 'delete',
                                              child: Row(
                                                children: [
                                                  Icon(Icons.delete, size: 16, color: Colors.red),
                                                  SizedBox(width: 8),
                                                  Text('Eliminar', style: TextStyle(color: Colors.red)),
                                                ],
                                              ),
                                            ),
                                          ],
                                          onSelected: (value) {
                                            if (value == 'edit') {
                                              _selectRolFromList(rolUser);
                                            } else if (value == 'delete') {
                                              _idController.text = rolUser.id.toString();
                                              _tabController.animateTo(2); // Switch to delete tab
                                            }
                                          },
                                        ),
                                        onTap: () => _selectRolFromList(rolUser),
                                      ),
                                    );
                                  },
                                ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
////
///TypeMovement widget
class TypeMovement {
  final int id;
  final String tipoMovimiento;

  TypeMovement({required this.id, required this.tipoMovimiento});
  
  factory TypeMovement.fromJson(Map<String, dynamic> json) =>
      TypeMovement(id: json['ID'], tipoMovimiento: json['TipoMovimiento']);
      
  Map<String, dynamic> toJson() => {
    'ID': id,
    'TipoMovimiento': tipoMovimiento,
  };
}

class TypeMovementCrudTabsWidget extends StatefulWidget {
  final String token;
  final VoidCallback onSuccess;

  const TypeMovementCrudTabsWidget({
    Key? key,
    required this.token,
    required this.onSuccess,
  }) : super(key: key);

  @override
  State<TypeMovementCrudTabsWidget> createState() => _TypeMovementCrudTabsWidgetState();
}

class _TypeMovementCrudTabsWidgetState extends State<TypeMovementCrudTabsWidget>
    with SingleTickerProviderStateMixin {
  final _formKey = GlobalKey<FormState>();
  final _idController = TextEditingController();
  final _tipoMovimientoController = TextEditingController();
  
  String? _output;
  List<TypeMovement> _typeMovements = [];
  bool _isLoading = false;
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 4, vsync: this);
    _consultar(); // Load data on init
  }

  @override
  void dispose() {
    _idController.dispose();
    _tipoMovimientoController.dispose();
    _tabController.dispose();
    super.dispose();
  }

  void _setLoading(bool loading) {
    setState(() {
      _isLoading = loading;
    });
  }

  void _showMessage(String message, {bool isError = false}) {
    setState(() {
      _output = message;
    });
    
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: isError ? Colors.red : Colors.green,
        duration: Duration(seconds: 3),
      ),
    );
  }

  void _clearForm() {
    _idController.clear();
    _tipoMovimientoController.clear();
    setState(() {
      _output = null;
    });
  }

  Future<void> _agregar() async {
    if (!_formKey.currentState!.validate()) return;
    
    final tipoMovimientoText = _tipoMovimientoController.text.trim();
    if (tipoMovimientoText.isEmpty) {
      _showMessage("El campo Tipo de Movimiento es requerido", isError: true);
      return;
    }

    _setLoading(true);
    
    try {
      // Get next available ID
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/typemovement/typemovements'),
        headers: {'Authorization': 'Bearer ${widget.token}'},
      );
      
      int nextId = 1;
      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body)['typemovements'];
        if (data.isNotEmpty) {
          nextId = data.map((e) => e['ID'] as int).reduce((a, b) => a > b ? a : b) + 1;
        }
      } else {
        _showMessage("Error al consultar tipos de movimiento: ${response.body}", isError: true);
        return;
      }

      // Create new movement type
      final createResponse = await http.post(
        Uri.parse('${AppConfig.baseUrl}/typemovement/create'),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Authorization': 'Bearer ${widget.token}',
        },
        body: {
          'ID': nextId.toString(),
          'TipoMovimiento': tipoMovimientoText,
        },
      );

      if (createResponse.statusCode == 201 || createResponse.statusCode == 200) {
        _showMessage("Tipo de movimiento creado exitosamente");
        _clearForm();
        await _consultar(); // Refresh the list
      } else {
        _showMessage("Error al crear tipo de movimiento: ${createResponse.body}", isError: true);
      }
    } catch (e) {
      _showMessage("Error de conexión: $e", isError: true);
    } finally {
      _setLoading(false);
    }
  }

  Future<void> _actualizar() async {
    if (!_formKey.currentState!.validate()) return;
    
    final idText = _idController.text.trim();
    final tipoMovimientoText = _tipoMovimientoController.text.trim();
    
    if (idText.isEmpty || tipoMovimientoText.isEmpty) {
      _showMessage("Todos los campos son requeridos", isError: true);
      return;
    }

    _setLoading(true);
    
    try {
      final response = await http.post(
        Uri.parse('${AppConfig.baseUrl}/typemovement/update'),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Authorization': 'Bearer ${widget.token}',
        },
        body: {
          'ID': idText,
          'TipoMovimiento': tipoMovimientoText,
        },
      );

      if (response.statusCode == 200) {
        _showMessage("Tipo de movimiento actualizado exitosamente");
        _clearForm();
        await _consultar(); // Refresh the list
      } else {
        _showMessage("Error al actualizar tipo de movimiento: ${response.body}", isError: true);
      }
    } catch (e) {
      _showMessage("Error de conexión: $e", isError: true);
    } finally {
      _setLoading(false);
    }
  }

  Future<void> _eliminar() async {
    final idText = _idController.text.trim();
    
    if (idText.isEmpty) {
      _showMessage("El campo ID es requerido", isError: true);
      return;
    }

    // Show confirmation dialog
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text("Confirmar eliminación"),
        content: Text("¿Está seguro de que desea eliminar el tipo de movimiento con ID $idText?"),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: Text("Cancelar"),
          ),
          TextButton(
            onPressed: () => Navigator.of(context).pop(true),
            style: TextButton.styleFrom(foregroundColor: Colors.red),
            child: Text("Eliminar"),
          ),
        ],
      ),
    );

    if (confirmed != true) return;

    _setLoading(true);
    
    try {
      final response = await http.post(
        Uri.parse('${AppConfig.baseUrl}/typemovement/delete'),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Authorization': 'Bearer ${widget.token}',
        },
        body: {
          'ID': idText,
        },
      );

      if (response.statusCode == 200) {
        _showMessage("Tipo de movimiento eliminado exitosamente");
        _clearForm();
      } else {
        _showMessage("Error al eliminar tipo de movimiento: ${response.body}", isError: true);
      }
    } catch (e) {
      _showMessage("Error de conexión: $e", isError: true);
    } finally {
      _setLoading(false);
    }
  }

  Future<void> _consultar() async {
    _setLoading(true);
    
    try {
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/typemovement/typemovements'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
        },
      );
      
      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body)['typemovements'];
        setState(() {
          _typeMovements = data.map((e) => TypeMovement.fromJson(e)).toList();
          _output = null;
        });
      } else {
        _showMessage("Error al consultar tipos de movimiento: ${response.body}", isError: true);
      }
    } catch (e) {
      _showMessage("Error de conexión: $e", isError: true);
    } finally {
      _setLoading(false);
    }
  }

  void _selectTypeMovementFromList(TypeMovement typeMovement) {
    setState(() {
      _idController.text = typeMovement.id.toString();
      _tipoMovimientoController.text = typeMovement.tipoMovimiento;
    });
    _tabController.animateTo(1); // Switch to update tab
  }

  Widget _buildLoadingOverlay({required Widget child}) {
    return Stack(
      children: [
        child,
        if (_isLoading)
          Container(
            color: Colors.black26,
            child: Center(
              child: CircularProgressIndicator(),
            ),
          ),
      ],
    );
  }

  Widget _buildFormField({
    required TextEditingController controller,
    required String label,
    TextInputType? keyboardType,
    String? Function(String?)? validator,
  }) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: TextFormField(
        controller: controller,
        decoration: InputDecoration(
          labelText: label,
          border: OutlineInputBorder(),
          contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        ),
        keyboardType: keyboardType,
        validator: validator,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 4,
      child: Column(
        children: [
          Container(
            decoration: BoxDecoration(
              color: Theme.of(context).cardColor,
              boxShadow: [
                BoxShadow(
                  color: Colors.black12,
                  blurRadius: 4,
                  offset: Offset(0, 2),
                ),
              ],
            ),
            child: TabBar(
              controller: _tabController,
              labelColor: Theme.of(context).primaryColor,
              unselectedLabelColor: Colors.grey,
              indicatorColor: Theme.of(context).primaryColor,
              tabs: [
                Tab(icon: Icon(Icons.add), text: "Agregar"),
                Tab(icon: Icon(Icons.edit), text: "Actualizar"),
                Tab(icon: Icon(Icons.delete), text: "Eliminar"),
                Tab(icon: Icon(Icons.list), text: "Consultar"),
              ],
            ),
          ),
          Expanded(
            child: _buildLoadingOverlay(
              child: TabBarView(
                controller: _tabController,
                children: [
                  // AGREGAR TAB
                  SingleChildScrollView(
                    padding: const EdgeInsets.all(16),
                    child: Form(
                      key: _formKey,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          Text(
                            "Crear Nuevo Tipo de Movimiento",
                            style: Theme.of(context).textTheme.headlineSmall,
                          ),
                          SizedBox(height: 16),
                          _buildFormField(
                            controller: _tipoMovimientoController,
                            label: "Tipo de Movimiento",
                            validator: (value) {
                              if (value == null || value.trim().isEmpty) {
                                return "Este campo es requerido";
                              }
                              if (value.trim().length < 2) {
                                return "El tipo de movimiento debe tener al menos 2 caracteres";
                              }
                              return null;
                            },
                          ),
                          SizedBox(height: 24),
                          ElevatedButton.icon(
                            onPressed: _isLoading ? null : _agregar,
                            icon: Icon(Icons.add),
                            label: Text("Crear Tipo de Movimiento"),
                            style: ElevatedButton.styleFrom(
                              padding: EdgeInsets.symmetric(vertical: 16),
                            ),
                          ),
                          if (_output != null) ...[
                            SizedBox(height: 16),
                            Container(
                              padding: EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: Colors.grey[100],
                                borderRadius: BorderRadius.circular(8),
                              ),
                              child: Text(
                                "Respuesta:\n$_output",
                                style: TextStyle(fontFamily: 'monospace'),
                              ),
                            ),
                          ],
                        ],
                      ),
                    ),
                  ),
                  
                  // ACTUALIZAR TAB
                  SingleChildScrollView(
                    padding: const EdgeInsets.all(16),
                    child: Form(
                      key: _formKey,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          Text(
                            "Actualizar Tipo de Movimiento",
                            style: Theme.of(context).textTheme.headlineSmall,
                          ),
                          SizedBox(height: 16),
                          _buildFormField(
                            controller: _idController,
                            label: "ID del Tipo de Movimiento",
                            keyboardType: TextInputType.number,
                            validator: (value) {
                              if (value == null || value.trim().isEmpty) {
                                return "Este campo es requerido";
                              }
                              if (int.tryParse(value.trim()) == null) {
                                return "Debe ser un número válido";
                              }
                              return null;
                            },
                          ),
                          _buildFormField(
                            controller: _tipoMovimientoController,
                            label: "Nuevo Tipo de Movimiento",
                            validator: (value) {
                              if (value == null || value.trim().isEmpty) {
                                return "Este campo es requerido";
                              }
                              if (value.trim().length < 2) {
                                return "El tipo de movimiento debe tener al menos 2 caracteres";
                              }
                              return null;
                            },
                          ),
                          SizedBox(height: 24),
                          ElevatedButton.icon(
                            onPressed: _isLoading ? null : _actualizar,
                            icon: Icon(Icons.update),
                            label: Text("Actualizar Tipo de Movimiento"),
                            style: ElevatedButton.styleFrom(
                              padding: EdgeInsets.symmetric(vertical: 16),
                            ),
                          ),
                          if (_output != null) ...[
                            SizedBox(height: 16),
                            Container(
                              padding: EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: Colors.grey[100],
                                borderRadius: BorderRadius.circular(8),
                              ),
                              child: Text(
                                "Respuesta:\n$_output",
                                style: TextStyle(fontFamily: 'monospace'),
                              ),
                            ),
                          ],
                        ],
                      ),
                    ),
                  ),
                  
                  // ELIMINAR TAB
                  SingleChildScrollView(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Text(
                          "Eliminar Tipo de Movimiento",
                          style: Theme.of(context).textTheme.headlineSmall,
                        ),
                        SizedBox(height: 16),
                        Container(
                          padding: EdgeInsets.all(12),
                          decoration: BoxDecoration(
                            color: Colors.red[50],
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(color: Colors.red[200]!),
                          ),
                          child: Row(
                            children: [
                              Icon(Icons.warning, color: Colors.red),
                              SizedBox(width: 8),
                              Expanded(
                                child: Text(
                                  "Esta acción no se puede deshacer",
                                  style: TextStyle(color: Colors.red[700]),
                                ),
                              ),
                            ],
                          ),
                        ),
                        SizedBox(height: 16),
                        _buildFormField(
                          controller: _idController,
                          label: "ID del Tipo de Movimiento a Eliminar",
                          keyboardType: TextInputType.number,
                        ),
                        SizedBox(height: 24),
                        ElevatedButton.icon(
                          onPressed: _isLoading ? null : _eliminar,
                          icon: Icon(Icons.delete),
                          label: Text("Eliminar Tipo de Movimiento"),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.red,
                            foregroundColor: Colors.white,
                            padding: EdgeInsets.symmetric(vertical: 16),
                          ),
                        ),
                        if (_output != null) ...[
                          SizedBox(height: 16),
                          Container(
                            padding: EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: Colors.grey[100],
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: Text(
                              "Respuesta:\n$_output",
                              style: TextStyle(fontFamily: 'monospace'),
                            ),
                          ),
                        ],
                      ],
                    ),
                  ),
                  
                  // CONSULTAR TAB
                  Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              "Lista de Tipos de Movimiento",
                              style: Theme.of(context).textTheme.headlineSmall,
                            ),
                            IconButton(
                              onPressed: _isLoading ? null : _consultar,
                              icon: Icon(Icons.refresh),
                              tooltip: "Actualizar lista",
                            ),
                          ],
                        ),
                        SizedBox(height: 16),
                        Expanded(
                          child: _typeMovements.isEmpty
                              ? Center(
                                  child: Column(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      Icon(
                                        Icons.inbox,
                                        size: 64,
                                        color: Colors.grey,
                                      ),
                                      SizedBox(height: 16),
                                      Text(
                                        "No hay tipos de movimiento para mostrar",
                                        style: TextStyle(
                                          fontSize: 16,
                                          color: Colors.grey[600],
                                        ),
                                      ),
                                      SizedBox(height: 8),
                                      TextButton.icon(
                                        onPressed: _consultar,
                                        icon: Icon(Icons.refresh),
                                        label: Text("Recargar"),
                                      ),
                                    ],
                                  ),
                                )
                              : ListView.builder(
                                  itemCount: _typeMovements.length,
                                  itemBuilder: (context, index) {
                                    final typeMovement = _typeMovements[index];
                                    return Card(
                                      margin: EdgeInsets.symmetric(vertical: 4),
                                      child: ListTile(
                                        leading: CircleAvatar(
                                          child: Text('${typeMovement.id}'),
                                          backgroundColor: Theme.of(context).primaryColor,
                                          foregroundColor: Colors.white,
                                        ),
                                        title: Text(
                                          typeMovement.tipoMovimiento,
                                          style: TextStyle(fontWeight: FontWeight.w500),
                                        ),
                                        subtitle: Text('ID: ${typeMovement.id}'),
                                        trailing: PopupMenuButton(
                                          itemBuilder: (context) => [
                                            PopupMenuItem(
                                              value: 'edit',
                                              child: Row(
                                                children: [
                                                  Icon(Icons.edit, size: 16),
                                                  SizedBox(width: 8),
                                                  Text('Editar'),
                                                ],
                                              ),
                                            ),
                                            PopupMenuItem(
                                              value: 'delete',
                                              child: Row(
                                                children: [
                                                  Icon(Icons.delete, size: 16, color: Colors.red),
                                                  SizedBox(width: 8),
                                                  Text('Eliminar', style: TextStyle(color: Colors.red)),
                                                ],
                                              ),
                                            ),
                                          ],
                                          onSelected: (value) {
                                            if (value == 'edit') {
                                              _selectTypeMovementFromList(typeMovement);
                                            } else if (value == 'delete') {
                                              _idController.text = typeMovement.id.toString();
                                              _tabController.animateTo(2); // Switch to delete tab
                                            }
                                          },
                                        ),
                                        onTap: () => _selectTypeMovementFromList(typeMovement),
                                      ),
                                    );
                                  },
                                ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
////
///Type Movement Widget
class TypeTransport {
  final int id;
  final String tipoTransporte;

  TypeTransport({required this.id, required this.tipoTransporte});
  
  factory TypeTransport.fromJson(Map<String, dynamic> json) =>
      TypeTransport(id: json['ID'], tipoTransporte: json['TipoTransporte']);
      
  Map<String, dynamic> toJson() => {
    'ID': id,
    'TipoTransporte': tipoTransporte,
  };
}

class TypeTransportCrudTabsWidget extends StatefulWidget {
  final String token;
  final VoidCallback onSuccess;

  const TypeTransportCrudTabsWidget({
    Key? key,
    required this.token,
    required this.onSuccess,
  }) : super(key: key);

  @override
  State<TypeTransportCrudTabsWidget> createState() => _TypeTransportCrudTabsWidgetState();
}

class _TypeTransportCrudTabsWidgetState extends State<TypeTransportCrudTabsWidget>
    with SingleTickerProviderStateMixin {
  final _formKey = GlobalKey<FormState>();
  final _idController = TextEditingController();
  final _tipoTransporteController = TextEditingController();
  
  String? _output;
  List<TypeTransport> _typeTransports = [];
  bool _isLoading = false;
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 4, vsync: this);
    _consultar(); // Load data on init
  }

  @override
  void dispose() {
    _idController.dispose();
    _tipoTransporteController.dispose();
    _tabController.dispose();
    super.dispose();
  }

  void _setLoading(bool loading) {
    setState(() {
      _isLoading = loading;
    });
  }

  void _showMessage(String message, {bool isError = false}) {
    setState(() {
      _output = message;
    });
    
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: isError ? Colors.red : Colors.green,
        duration: Duration(seconds: 3),
      ),
    );
  }

  void _clearForm() {
    _idController.clear();
    _tipoTransporteController.clear();
    setState(() {
      _output = null;
    });
  }

  Future<void> _agregar() async {
    if (!_formKey.currentState!.validate()) return;
    
    final tipoTransporteText = _tipoTransporteController.text.trim();
    if (tipoTransporteText.isEmpty) {
      _showMessage("El campo Tipo de Transporte es requerido", isError: true);
      return;
    }

    _setLoading(true);
    
    try {
      // Get next available ID
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/typetransport/typetransports'),
        headers: {'Authorization': 'Bearer ${widget.token}'},
      );
      
      int nextId = 1;
      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body)['typetransports'];
        if (data.isNotEmpty) {
          nextId = data.map((e) => e['ID'] as int).reduce((a, b) => a > b ? a : b) + 1;
        }
      } else {
        _showMessage("Error al consultar tipos de transporte: ${response.body}", isError: true);
        return;
      }

      // Create new transport type
      final createResponse = await http.post(
        Uri.parse('${AppConfig.baseUrl}/typetransport/create'),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Authorization': 'Bearer ${widget.token}',
        },
        body: {
          'ID': nextId.toString(),
          'TipoTransporte': tipoTransporteText,
        },
      );

      if (createResponse.statusCode == 201 || createResponse.statusCode == 200) {
        _showMessage("Tipo de transporte creado exitosamente");
        _clearForm();
        await _consultar(); // Refresh the list
      } else {
        _showMessage("Error al crear tipo de transporte: ${createResponse.body}", isError: true);
      }
    } catch (e) {
      _showMessage("Error de conexión: $e", isError: true);
    } finally {
      _setLoading(false);
    }
  }

  Future<void> _actualizar() async {
    if (!_formKey.currentState!.validate()) return;
    
    final idText = _idController.text.trim();
    final tipoTransporteText = _tipoTransporteController.text.trim();
    
    if (idText.isEmpty || tipoTransporteText.isEmpty) {
      _showMessage("Todos los campos son requeridos", isError: true);
      return;
    }

    _setLoading(true);
    
    try {
      final response = await http.post(
        Uri.parse('${AppConfig.baseUrl}/typetransport/update'),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Authorization': 'Bearer ${widget.token}',
        },
        body: {
          'ID': idText,
          'TipoTransporte': tipoTransporteText,
        },
      );

      if (response.statusCode == 200) {
        _showMessage("Tipo de transporte actualizado exitosamente");
        _clearForm();
        await _consultar(); // Refresh the list
      } else {
        _showMessage("Error al actualizar tipo de transporte: ${response.body}", isError: true);
      }
    } catch (e) {
      _showMessage("Error de conexión: $e", isError: true);
    } finally {
      _setLoading(false);
    }
  }

  Future<void> _eliminar() async {
    final idText = _idController.text.trim();
    
    if (idText.isEmpty) {
      _showMessage("El campo ID es requerido", isError: true);
      return;
    }

    // Show confirmation dialog
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text("Confirmar eliminación"),
        content: Text("¿Está seguro de que desea eliminar el tipo de transporte con ID $idText?"),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: Text("Cancelar"),
          ),
          TextButton(
            onPressed: () => Navigator.of(context).pop(true),
            style: TextButton.styleFrom(foregroundColor: Colors.red),
            child: Text("Eliminar"),
          ),
        ],
      ),
    );

    if (confirmed != true) return;

    _setLoading(true);
    
    try {
      final response = await http.post(
        Uri.parse('${AppConfig.baseUrl}/typetransport/delete'),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Authorization': 'Bearer ${widget.token}',
        },
        body: {
          'ID': idText,
        },
      );

      if (response.statusCode == 200) {
        _showMessage("Tipo de transporte eliminado exitosamente");
        _clearForm();
        await _consultar(); // Refresh the list
      } else {
        _showMessage("Error al eliminar tipo de transporte: ${response.body}", isError: true);
      }
    } catch (e) {
      _showMessage("Error de conexión: $e", isError: true);
    } finally {
      _setLoading(false);
    }
  }

  Future<void> _consultar() async {
    _setLoading(true);
    
    try {
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/typetransport/typetransports'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
        },
      );
      
      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body)['typetransports'];
        setState(() {
          _typeTransports = data.map((e) => TypeTransport.fromJson(e)).toList();
          _output = null;
        });
      } else {
        _showMessage("Error al consultar tipos de transporte: ${response.body}", isError: true);
      }
    } catch (e) {
      _showMessage("Error de conexión: $e", isError: true);
    } finally {
      _setLoading(false);
    }
  }

  void _selectTypeTransportFromList(TypeTransport typeTransport) {
    setState(() {
      _idController.text = typeTransport.id.toString();
      _tipoTransporteController.text = typeTransport.tipoTransporte;
    });
    _tabController.animateTo(1); // Switch to update tab
  }

  Widget _buildLoadingOverlay({required Widget child}) {
    return Stack(
      children: [
        child,
        if (_isLoading)
          Container(
            color: Colors.black26,
            child: Center(
              child: CircularProgressIndicator(),
            ),
          ),
      ],
    );
  }

  Widget _buildFormField({
    required TextEditingController controller,
    required String label,
    TextInputType? keyboardType,
    String? Function(String?)? validator,
    IconData? prefixIcon,
  }) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: TextFormField(
        controller: controller,
        decoration: InputDecoration(
          labelText: label,
          prefixIcon: prefixIcon != null ? Icon(prefixIcon) : null,
          border: OutlineInputBorder(),
          contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        ),
        keyboardType: keyboardType,
        validator: validator,
      ),
    );
  }

  IconData _getTransportIcon(String transportType) {
    final type = transportType.toLowerCase();
    if (type.contains('auto') || type.contains('carro') || type.contains('vehiculo')) {
      return Icons.directions_car;
    } else if (type.contains('bus') || type.contains('autobus')) {
      return Icons.directions_bus;
    } else if (type.contains('tren') || type.contains('metro')) {
      return Icons.train;
    } else if (type.contains('avion') || type.contains('aereo')) {
      return Icons.flight;
    } else if (type.contains('barco') || type.contains('maritimo')) {
      return Icons.directions_boat;
    } else if (type.contains('bici') || type.contains('cicla')) {
      return Icons.directions_bike;
    } else if (type.contains('camion') || type.contains('truck')) {
      return Icons.local_shipping;
    } else {
      return Icons.directions;
    }
  }

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 4,
      child: Column(
        children: [
          Container(
            decoration: BoxDecoration(
              color: Theme.of(context).cardColor,
              boxShadow: [
                BoxShadow(
                  color: Colors.black12,
                  blurRadius: 4,
                  offset: Offset(0, 2),
                ),
              ],
            ),
            child: TabBar(
              controller: _tabController,
              labelColor: Theme.of(context).primaryColor,
              unselectedLabelColor: Colors.grey,
              indicatorColor: Theme.of(context).primaryColor,
              tabs: [
                Tab(icon: Icon(Icons.add), text: "Agregar"),
                Tab(icon: Icon(Icons.edit), text: "Actualizar"),
                Tab(icon: Icon(Icons.delete), text: "Eliminar"),
                Tab(icon: Icon(Icons.list), text: "Consultar"),
              ],
            ),
          ),
          Expanded(
            child: _buildLoadingOverlay(
              child: TabBarView(
                controller: _tabController,
                children: [
                  // AGREGAR TAB
                  SingleChildScrollView(
                    padding: const EdgeInsets.all(16),
                    child: Form(
                      key: _formKey,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          Text(
                            "Crear Nuevo Tipo de Transporte",
                            style: Theme.of(context).textTheme.headlineSmall,
                          ),
                          SizedBox(height: 16),
                          _buildFormField(
                            controller: _tipoTransporteController,
                            label: "Tipo de Transporte",
                            prefixIcon: Icons.directions,
                            validator: (value) {
                              if (value == null || value.trim().isEmpty) {
                                return "Este campo es requerido";
                              }
                              if (value.trim().length < 2) {
                                return "El tipo de transporte debe tener al menos 2 caracteres";
                              }
                              return null;
                            },
                          ),
                          SizedBox(height: 24),
                          ElevatedButton.icon(
                            onPressed: _isLoading ? null : _agregar,
                            icon: Icon(Icons.add),
                            label: Text("Crear Tipo de Transporte"),
                            style: ElevatedButton.styleFrom(
                              padding: EdgeInsets.symmetric(vertical: 16),
                            ),
                          ),
                          if (_output != null) ...[
                            SizedBox(height: 16),
                            Container(
                              padding: EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: Colors.grey[100],
                                borderRadius: BorderRadius.circular(8),
                              ),
                              child: Text(
                                "Respuesta:\n$_output",
                                style: TextStyle(fontFamily: 'monospace'),
                              ),
                            ),
                          ],
                        ],
                      ),
                    ),
                  ),
                  
                  // ACTUALIZAR TAB
                  SingleChildScrollView(
                    padding: const EdgeInsets.all(16),
                    child: Form(
                      key: _formKey,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          Text(
                            "Actualizar Tipo de Transporte",
                            style: Theme.of(context).textTheme.headlineSmall,
                          ),
                          SizedBox(height: 16),
                          _buildFormField(
                            controller: _idController,
                            label: "ID del Tipo de Transporte",
                            prefixIcon: Icons.tag,
                            keyboardType: TextInputType.number,
                            validator: (value) {
                              if (value == null || value.trim().isEmpty) {
                                return "Este campo es requerido";
                              }
                              if (int.tryParse(value.trim()) == null) {
                                return "Debe ser un número válido";
                              }
                              return null;
                            },
                          ),
                          _buildFormField(
                            controller: _tipoTransporteController,
                            label: "Nuevo Tipo de Transporte",
                            prefixIcon: Icons.directions,
                            validator: (value) {
                              if (value == null || value.trim().isEmpty) {
                                return "Este campo es requerido";
                              }
                              if (value.trim().length < 2) {
                                return "El tipo de transporte debe tener al menos 2 caracteres";
                              }
                              return null;
                            },
                          ),
                          SizedBox(height: 24),
                          ElevatedButton.icon(
                            onPressed: _isLoading ? null : _actualizar,
                            icon: Icon(Icons.update),
                            label: Text("Actualizar Tipo de Transporte"),
                            style: ElevatedButton.styleFrom(
                              padding: EdgeInsets.symmetric(vertical: 16),
                            ),
                          ),
                          if (_output != null) ...[
                            SizedBox(height: 16),
                            Container(
                              padding: EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: Colors.grey[100],
                                borderRadius: BorderRadius.circular(8),
                              ),
                              child: Text(
                                "Respuesta:\n$_output",
                                style: TextStyle(fontFamily: 'monospace'),
                              ),
                            ),
                          ],
                        ],
                      ),
                    ),
                  ),
                  
                  // ELIMINAR TAB
                  SingleChildScrollView(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Text(
                          "Eliminar Tipo de Transporte",
                          style: Theme.of(context).textTheme.headlineSmall,
                        ),
                        SizedBox(height: 16),
                        Container(
                          padding: EdgeInsets.all(12),
                          decoration: BoxDecoration(
                            color: Colors.red[50],
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(color: Colors.red[200]!),
                          ),
                          child: Row(
                            children: [
                              Icon(Icons.warning, color: Colors.red),
                              SizedBox(width: 8),
                              Expanded(
                                child: Text(
                                  "Esta acción no se puede deshacer",
                                  style: TextStyle(color: Colors.red[700]),
                                ),
                              ),
                            ],
                          ),
                        ),
                        SizedBox(height: 16),
                        _buildFormField(
                          controller: _idController,
                          label: "ID del Tipo de Transporte a Eliminar",
                          prefixIcon: Icons.tag,
                          keyboardType: TextInputType.number,
                        ),
                        SizedBox(height: 24),
                        ElevatedButton.icon(
                          onPressed: _isLoading ? null : _eliminar,
                          icon: Icon(Icons.delete),
                          label: Text("Eliminar Tipo de Transporte"),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.red,
                            foregroundColor: Colors.white,
                            padding: EdgeInsets.symmetric(vertical: 16),
                          ),
                        ),
                        if (_output != null) ...[
                          SizedBox(height: 16),
                          Container(
                            padding: EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: Colors.grey[100],
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: Text(
                              "Respuesta:\n$_output",
                              style: TextStyle(fontFamily: 'monospace'),
                            ),
                          ),
                        ],
                      ],
                    ),
                  ),
                  
                  // CONSULTAR TAB
                  Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              "Lista de Tipos de Transporte",
                              style: Theme.of(context).textTheme.headlineSmall,
                            ),
                            IconButton(
                              onPressed: _isLoading ? null : _consultar,
                              icon: Icon(Icons.refresh),
                              tooltip: "Actualizar lista",
                            ),
                          ],
                        ),
                        SizedBox(height: 16),
                        Expanded(
                          child: _typeTransports.isEmpty
                              ? Center(
                                  child: Column(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      Icon(
                                        Icons.directions,
                                        size: 64,
                                        color: Colors.grey,
                                      ),
                                      SizedBox(height: 16),
                                      Text(
                                        "No hay tipos de transporte para mostrar",
                                        style: TextStyle(
                                          fontSize: 16,
                                          color: Colors.grey[600],
                                        ),
                                      ),
                                      SizedBox(height: 8),
                                      TextButton.icon(
                                        onPressed: _consultar,
                                        icon: Icon(Icons.refresh),
                                        label: Text("Recargar"),
                                      ),
                                    ],
                                  ),
                                )
                              : ListView.builder(
                                  itemCount: _typeTransports.length,
                                  itemBuilder: (context, index) {
                                    final typeTransport = _typeTransports[index];
                                    final transportIcon = _getTransportIcon(typeTransport.tipoTransporte);
                                    
                                    return Card(
                                      margin: EdgeInsets.symmetric(vertical: 4),
                                      child: ListTile(
                                        leading: CircleAvatar(
                                          child: Icon(transportIcon, color: Colors.white),
                                          backgroundColor: Theme.of(context).primaryColor,
                                        ),
                                        title: Text(
                                          typeTransport.tipoTransporte,
                                          style: TextStyle(fontWeight: FontWeight.w500),
                                        ),
                                        subtitle: Text('ID: ${typeTransport.id}'),
                                        trailing: PopupMenuButton(
                                          itemBuilder: (context) => [
                                            PopupMenuItem(
                                              value: 'edit',
                                              child: Row(
                                                children: [
                                                  Icon(Icons.edit, size: 16),
                                                  SizedBox(width: 8),
                                                  Text('Editar'),
                                                ],
                                              ),
                                            ),
                                            PopupMenuItem(
                                              value: 'delete',
                                              child: Row(
                                                children: [
                                                  Icon(Icons.delete, size: 16, color: Colors.red),
                                                  SizedBox(width: 8),
                                                  Text('Eliminar', style: TextStyle(color: Colors.red)),
                                                ],
                                              ),
                                            ),
                                          ],
                                          onSelected: (value) {
                                            if (value == 'edit') {
                                              _selectTypeTransportFromList(typeTransport);
                                            } else if (value == 'delete') {
                                              _idController.text = typeTransport.id.toString();
                                              _tabController.animateTo(2); // Switch to delete tab
                                            }
                                          },
                                        ),
                                        onTap: () => _selectTypeTransportFromList(typeTransport),
                                      ),
                                    );
                                  },
                                ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
////
///PRICE CRUD SERVICE
///CREATE
class CreatePriceWidget extends StatefulWidget {
  final String token;
  final VoidCallback? onSuccess;
  final VoidCallback? onCancel;

  const CreatePriceWidget({
    Key? key,
    required this.token,
    this.onSuccess,
    this.onCancel,
  }) : super(key: key);

  @override
  State<CreatePriceWidget> createState() => _CreatePriceWidgetState();
}

class _CreatePriceWidgetState extends State<CreatePriceWidget> {
  final _formKey = GlobalKey<FormState>();
  final _montoController = TextEditingController();

  int? _newId;
  List<TypeTransport> _typeTransports = [];
  TypeTransport? _selectedTransport;
  bool _loading = true;
  bool _submitting = false;
  String? _message;
  bool _success = false;

  @override
  void initState() {
    super.initState();
    _initData();
  }

  @override
  void dispose() {
    _montoController.dispose();
    super.dispose();
  }

  Future<void> _initData() async {
    setState(() => _loading = true);
    try {
      await _fetchTypeTransports();
      await _fetchLastId();
    } catch (e) {
      _showMessage("Error al cargar datos iniciales: $e", isError: true);
    } finally {
      setState(() => _loading = false);
    }
  }

  Future<void> _fetchTypeTransports() async {
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/typetransport/typetransports'),
      headers: {'Authorization': 'Bearer ${widget.token}'},
    );
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      final rawList = data['typetransports'] ?? [];
      _typeTransports = List<TypeTransport>.from(
        rawList.map((e) => TypeTransport.fromJson(e)),
      );
      if (_typeTransports.isNotEmpty) {
        _selectedTransport = _typeTransports.first;
      }
    } else {
      throw Exception('Error tipos de transporte: ${response.statusCode}');
    }
  }

  Future<void> _fetchLastId() async {
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/price/administrador/prices'),
      headers: {'Authorization': 'Bearer ${widget.token}'},
    );
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      final List<dynamic> prices = data['prices'] ?? [];
      final lastId = prices.isNotEmpty
          ? (prices.map((e) => e['ID'] ?? 0).reduce((a, b) => a > b ? a : b))
          : 0;
      _newId = lastId + 1;
    } else {
      _newId = 1;
    }
  }

  void _showMessage(String message, {bool isError = false}) {
    setState(() {
      _message = message;
      _success = !isError;
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: isError ? Colors.red : Colors.green,
      ),
    );
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate() || _selectedTransport == null) {
      _showMessage("Complete todos los campos correctamente", isError: true);
      return;
    }
    final monto = double.tryParse(_montoController.text);
    if (monto == null || monto <= 0) {
      _showMessage("Ingrese un monto válido", isError: true);
      return;
    }

    setState(() {
      _submitting = true;
      _message = null;
    });

    try {
      final uri = Uri.parse('${AppConfig.baseUrl}/price/create');
      final request = http.MultipartRequest('POST', uri)
        ..headers['Authorization'] = 'Bearer ${widget.token}'
        ..fields['ID'] = _newId.toString()
        ..fields['IDTipoTransporte'] = _selectedTransport!.id.toString()
        ..fields['Monto'] = monto.toStringAsFixed(2);

      final streamedResponse = await request.send();
      final resp = await http.Response.fromStream(streamedResponse);

      final data = json.decode(resp.body);
      if (resp.statusCode == 201 && data['success'] == true) {
        _showMessage("¡Precio creado!");
        _clearForm();
        await _fetchLastId();
        widget.onSuccess?.call();
      } else {
        _showMessage(data['detail'] ?? data['message'] ?? "Error al crear tarifa", isError: true);
      }
    } catch (e) {
      _showMessage("Error de conexión: $e", isError: true);
    } finally {
      setState(() => _submitting = false);
    }
  }

  void _clearForm() {
    _montoController.clear();
    if (_typeTransports.isNotEmpty) {
      setState(() {
        _selectedTransport = _typeTransports.first;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return Center(child: CircularProgressIndicator());
    }
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Form(
        key: _formKey,
        child: ListView(
          shrinkWrap: true,
          children: [
            Text('ID: ${_newId ?? "Cargando..."}', style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            DropdownButtonFormField<TypeTransport>(
              decoration: InputDecoration(
                labelText: 'Tipo de Transporte',
                border: OutlineInputBorder(),
              ),
              value: _selectedTransport,
              items: _typeTransports
                  .map((t) => DropdownMenuItem<TypeTransport>(
                        value: t,
                        child: Text('${t.tipoTransporte} (ID: ${t.id})'),
                      ))
                  .toList(),
              onChanged: (t) => setState(() => _selectedTransport = t),
              validator: (v) => v == null ? 'Seleccione un tipo de transporte' : null,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _montoController,
              keyboardType: TextInputType.numberWithOptions(decimal: true),
              inputFormatters: [FilteringTextInputFormatter.allow(RegExp(r'^\d+\.?\d{0,2}'))],
              decoration: InputDecoration(
                labelText: 'Monto',
                suffixText: 'USD',
                border: OutlineInputBorder(),
                helperText: 'Ingrese el precio en dólares',
              ),
              validator: (value) {
                if (value == null || value.isEmpty) return 'Ingrese el monto';
                final amount = double.tryParse(value);
                if (amount == null) return 'Monto inválido';
                if (amount <= 0) return 'El monto debe ser mayor a 0';
                if (amount > 999999) return 'Monto demasiado alto';
                return null;
              },
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: ElevatedButton(
                    onPressed: _submitting ? null : _submit,
                    child: _submitting
                        ? SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2))
                        : Text('Crear Tarifa'),
                  ),
                ),
                if (widget.onCancel != null)
                  Expanded(
                    child: TextButton(
                      onPressed: widget.onCancel,
                      child: Text('Cancelar'),
                    ),
                  ),
              ],
            ),
            if (_message != null)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 8),
                child: Text(
                  _message!,
                  style: TextStyle(
                    color: _success ? Colors.green : Colors.red,
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
///UPDATE
// MODELOS
class PriceData {
  final int id;
  final int idTipoTransporte;
  final double monto;

  PriceData({
    required this.id,
    required this.idTipoTransporte,
    required this.monto,
  });

  factory PriceData.fromJson(Map<String, dynamic> json) => PriceData(
        id: json['ID'],
        idTipoTransporte: json['IDTipoTransporte'],
        monto: (json['Monto'] is int)
            ? (json['Monto'] as int).toDouble()
            : (json['Monto'] as double),
      );
}

// ROOT FLOW
class UpdatePriceFlow extends StatefulWidget {
  final String token;
  final VoidCallback? onCancel;
  final VoidCallback? onSuccess;

  const UpdatePriceFlow({
    super.key,
    required this.token,
    this.onCancel,
    this.onSuccess,
  });

  @override
  State<UpdatePriceFlow> createState() => _UpdatePriceFlowState();
}

class _UpdatePriceFlowState extends State<UpdatePriceFlow> {
  int? _priceId;

  @override
  Widget build(BuildContext context) {
    return _priceId == null
        ? _IdPromptWidget(onIdEntered: (id) => setState(() => _priceId = id))
        : UpdatePriceWidget(
            token: widget.token,
            id: _priceId!,
            onCancel: widget.onCancel,
            onSuccess: widget.onSuccess,
          );
  }
}

// ID PROMPT
class _IdPromptWidget extends StatefulWidget {
  final void Function(int id) onIdEntered;
  const _IdPromptWidget({required this.onIdEntered});

  @override
  State<_IdPromptWidget> createState() => _IdPromptWidgetState();
}

class _IdPromptWidgetState extends State<_IdPromptWidget> {
  final _controller = TextEditingController();
  String? _error;

  void _submit() {
    final id = int.tryParse(_controller.text.trim());
    if (id != null && id > 0) {
      widget.onIdEntered(id);
    } else {
      setState(() => _error = 'Ingrese un ID válido');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text("ID del precio a editar:"),
          const SizedBox(height: 8),
          TextField(
            controller: _controller,
            keyboardType: TextInputType.number,
            decoration: InputDecoration(
              labelText: "ID de precio",
              errorText: _error,
              border: OutlineInputBorder(),
            ),
            onSubmitted: (_) => _submit(),
          ),
          const SizedBox(height: 8),
          ElevatedButton(
            onPressed: _submit,
            child: const Text("Buscar"),
          ),
        ],
      ),
    );
  }
}

// UPDATE WIDGET
class UpdatePriceWidget extends StatefulWidget {
  final String token;
  final int id;
  final VoidCallback? onSuccess;
  final VoidCallback? onCancel;

  const UpdatePriceWidget({
    Key? key,
    required this.token,
    required this.id,
    this.onSuccess,
    this.onCancel,
  }) : super(key: key);

  @override
  State<UpdatePriceWidget> createState() => _UpdatePriceWidgetState();
}

class _UpdatePriceWidgetState extends State<UpdatePriceWidget> {
  final _formKey = GlobalKey<FormState>();
  final _montoController = TextEditingController();

  List<TypeTransport> _typeTransports = [];
  TypeTransport? _selectedTransport;
  PriceData? _originalPrice;
  bool _loading = true;
  bool _submitting = false;
  String? _message;
  bool _success = false;
  bool _hasChanges = false;

  @override
  void initState() {
    super.initState();
    _initData();
    _montoController.addListener(_checkForChanges);
  }

  @override
  void dispose() {
    _montoController.dispose();
    super.dispose();
  }

  Future<void> _initData() async {
    setState(() => _loading = true);
    try {
      await _fetchTypeTransports();
      await _fetchPriceData();
    } catch (e) {
      _showMessage("Error al cargar datos: $e", isError: true);
    } finally {
      setState(() => _loading = false);
    }
  }

  Future<void> _fetchTypeTransports() async {
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/typetransport/typetransports'),
      headers: {'Authorization': 'Bearer ${widget.token}'},
    );
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      final rawList = data['typetransports'] ?? [];
      _typeTransports = List<TypeTransport>.from(
        rawList.map((e) => TypeTransport.fromJson(e)),
      );
    } else {
      throw Exception('Tipos de transporte: ${response.statusCode}');
    }
  }

  Future<void> _fetchPriceData() async {
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/price/administrador/precio?id=${widget.id}'),
      headers: {'Authorization': 'Bearer ${widget.token}'},
    );
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      _originalPrice = PriceData.fromJson(data);
      _montoController.text = _originalPrice!.monto.toStringAsFixed(2);
      _selectedTransport = _typeTransports.firstWhere(
        (tt) => tt.id == _originalPrice!.idTipoTransporte,
        orElse: () => _typeTransports.first,
      );
    } else {
      throw Exception('Precio no encontrado');
    }
  }

  void _checkForChanges() {
    if (_originalPrice == null) return;
    final currentMonto = double.tryParse(_montoController.text) ?? 0.0;
    final currentTransportId = _selectedTransport?.id ?? 0;
    final hasChanges = currentMonto != _originalPrice!.monto ||
        currentTransportId != _originalPrice!.idTipoTransporte;
    if (hasChanges != _hasChanges) {
      setState(() => _hasChanges = hasChanges);
    }
  }

  void _showMessage(String message, {bool isError = false}) {
    setState(() {
      _message = message;
      _success = !isError;
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: isError ? Colors.red : Colors.green,
      ),
    );
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate() || _selectedTransport == null) {
      _showMessage("Complete todos los campos correctamente", isError: true);
      return;
    }
    if (!_hasChanges) {
      _showMessage("No se han detectado cambios", isError: true);
      return;
    }
    final monto = double.tryParse(_montoController.text);
    if (monto == null || monto <= 0) {
      _showMessage("Ingrese un monto válido", isError: true);
      return;
    }
    if (!await _showConfirmationDialog()) return;

    setState(() {
      _submitting = true;
      _message = null;
    });

    try {
      final uri = Uri.parse('${AppConfig.baseUrl}/price/update');
      final request = http.MultipartRequest('POST', uri)
        ..headers['Authorization'] = 'Bearer ${widget.token}'
        ..fields['ID'] = widget.id.toString()
        ..fields['IDTipoTransporte'] = _selectedTransport!.id.toString()
        ..fields['Monto'] = monto.toStringAsFixed(2);

      final streamedResponse = await request.send();
      final resp = await http.Response.fromStream(streamedResponse);

      final data = json.decode(resp.body);
      if (resp.statusCode == 200 && data['success'] == true) {
        _showMessage("¡Precio actualizado!");
        await _fetchPriceData();
        widget.onSuccess?.call();
      } else {
        _showMessage(data['detail'] ?? data['message'] ?? "Error al actualizar precio", isError: true);
      }
    } catch (e) {
      _showMessage("Error de conexión: $e", isError: true);
    } finally {
      setState(() => _submitting = false);
    }
  }

  Future<bool> _showConfirmationDialog() async {
    final originalMonto = _originalPrice?.monto ?? 0.0;
    final newMonto = double.tryParse(_montoController.text) ?? 0.0;
    final difference = newMonto - originalMonto;

    return await showDialog<bool>(
          context: context,
          builder: (context) => AlertDialog(
            title: Text("Confirmar"),
            content: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text("¿Actualizar el precio?"),
                SizedBox(height: 8),
                Text("Antes: \$${originalMonto.toStringAsFixed(2)}"),
                Text("Nuevo: \$${newMonto.toStringAsFixed(2)}"),
                Text("Diferencia: ${difference >= 0 ? '+' : ''}\$${difference.toStringAsFixed(2)}"),
              ],
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.of(context).pop(false),
                child: Text("Cancelar"),
              ),
              ElevatedButton(
                onPressed: () => Navigator.of(context).pop(true),
                child: Text("Confirmar"),
              ),
            ],
          ),
        ) ??
        false;
  }

  void _resetForm() {
    if (_originalPrice != null) {
      _montoController.text = _originalPrice!.monto.toStringAsFixed(2);
      setState(() {
        _selectedTransport = _typeTransports.firstWhere(
          (tt) => tt.id == _originalPrice!.idTipoTransporte,
          orElse: () => _typeTransports.first,
        );
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return Center(child: CircularProgressIndicator());
    }
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Form(
        key: _formKey,
        child: ListView(
          shrinkWrap: true,
          children: [
            Text('ID: ${widget.id}', style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            DropdownButtonFormField<TypeTransport>(
              decoration: InputDecoration(
                labelText: 'Tipo de Transporte',
                border: OutlineInputBorder(),
              ),
              value: _selectedTransport,
              items: _typeTransports
                  .map((t) => DropdownMenuItem<TypeTransport>(
                        value: t,
                        child: Text('${t.tipoTransporte} (ID: ${t.id})'),
                      ))
                  .toList(),
              onChanged: (t) {
                setState(() => _selectedTransport = t);
                _checkForChanges();
              },
              validator: (v) => v == null ? 'Seleccione un tipo de transporte' : null,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _montoController,
              keyboardType: TextInputType.numberWithOptions(decimal: true),
              inputFormatters: [FilteringTextInputFormatter.allow(RegExp(r'^\d+\.?\d{0,2}'))],
              decoration: InputDecoration(
                labelText: 'Monto',
                suffixText: 'USD',
                border: OutlineInputBorder(),
                helperText: _originalPrice != null
                    ? 'Monto original: \$${_originalPrice!.monto.toStringAsFixed(2)}'
                    : null,
              ),
              validator: (value) {
                if (value == null || value.isEmpty) return 'Ingrese el monto';
                final amount = double.tryParse(value);
                if (amount == null) return 'Monto inválido';
                if (amount <= 0) return 'El monto debe ser mayor a 0';
                if (amount > 999999) return 'Monto demasiado alto';
                return null;
              },
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: OutlinedButton(
                    onPressed: _resetForm,
                    child: Text('Restablecer'),
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: ElevatedButton(
                    onPressed: (_submitting || !_hasChanges) ? null : _submit,
                    child: _submitting ? SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2)) : Text('Actualizar'),
                  ),
                ),
              ],
            ),
            if (widget.onCancel != null)
              TextButton(
                onPressed: widget.onCancel,
                child: Text('Cancelar'),
              ),
            if (_message != null)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 8),
                child: Text(
                  _message!,
                  style: TextStyle(
                    color: _success ? Colors.green : Colors.red,
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
////DELETE
class DeletePriceWidget extends StatefulWidget {
  final String token;
  final VoidCallback? onSuccess;
  final VoidCallback? onCancel;

  const DeletePriceWidget({
    Key? key,
    required this.token,
    this.onSuccess,
    this.onCancel,
  }) : super(key: key);

  @override
  State<DeletePriceWidget> createState() => _DeletePriceWidgetState();
}

class _DeletePriceWidgetState extends State<DeletePriceWidget> {
  final _formKey = GlobalKey<FormState>();
  final _idController = TextEditingController();

  bool _loading = false;
  String? _message;
  bool _success = false;

  @override
  void dispose() {
    _idController.dispose();
    super.dispose();
  }

  Future<void> _deletePrice() async {
    final id = int.tryParse(_idController.text.trim());
    if (id == null || id < 0) {
      setState(() {
        _message = "Ingrese un ID válido";
        _success = false;
      });
      return;
    }
    setState(() {
      _loading = true;
      _message = null;
    });

    try {
      final uri = Uri.parse('${AppConfig.baseUrl}/price/delete');
      final request = http.MultipartRequest('POST', uri)
        ..headers['Authorization'] = 'Bearer ${widget.token}'
        ..fields['ID'] = id.toString();

      final streamedResponse = await request.send();
      final resp = await http.Response.fromStream(streamedResponse);
      final data = json.decode(resp.body);

      if (resp.statusCode == 200 && data['success'] == true) {
        setState(() {
          _message = data['message'] ?? "Eliminado exitosamente.";
          _success = true;
        });
        widget.onSuccess?.call();
      } else {
        setState(() {
          _message = data['detail'] ?? data['message'] ?? "Error al eliminar.";
          _success = false;
        });
      }
    } catch (e) {
      setState(() {
        _message = "Error de conexión: $e";
        _success = false;
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Form(
        key: _formKey,
        child: ListView(
          shrinkWrap: true,
          children: [
            Text(
              'Eliminar Precio',
              style: Theme.of(context).textTheme.headlineLarge,
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _idController,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(
                labelText: 'ID de precio a eliminar',
                border: OutlineInputBorder(),
              ),
              validator: (value) {
                final id = int.tryParse(value ?? '');
                if (id == null || id <= 0) return 'Ingrese un ID válido';
                return null;
              },
              enabled: !_loading,
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: ElevatedButton(
                    onPressed: _loading
                        ? null
                        : () {
                            if (_formKey.currentState?.validate() ?? false) {
                              _deletePrice();
                            }
                          },
                    child: _loading
                        ? SizedBox(
                            width: 16,
                            height: 16,
                            child: CircularProgressIndicator(strokeWidth: 2),
                          )
                        : Text('Eliminar'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.red,
                      foregroundColor: Colors.white,
                    ),
                  ),
                ),
                if (widget.onCancel != null)
                  Expanded(
                    child: TextButton(
                      onPressed: widget.onCancel,
                      child: Text('Cancelar'),
                    ),
                  ),
              ],
            ),
            if (_message != null)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 8),
                child: Text(
                  _message!,
                  style: TextStyle(
                    color: _success ? Colors.green : Colors.red,
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
////
///Consultar
// Modelo mínimo para el precio
class Price {
  final int id;
  final int idTipoTransporte;
  final double monto;

  Price({required this.id, required this.idTipoTransporte, required this.monto});

  factory Price.fromJson(Map<String, dynamic> json) => Price(
        id: json['ID'],
        idTipoTransporte: json['IDTipoTransporte'],
        monto: (json['Monto'] is int)
            ? (json['Monto'] as int).toDouble()
            : (json['Monto'] as double),
      );
}

class AdminPricesListWidget extends StatefulWidget {
  final String token;
  final VoidCallback? onRefresh;

  const AdminPricesListWidget({
    Key? key,
    required this.token,
    this.onRefresh,
  }) : super(key: key);

  @override
  State<AdminPricesListWidget> createState() => _AdminPricesListWidgetState();
}

class _AdminPricesListWidgetState extends State<AdminPricesListWidget> {
  List<Price>? _prices;
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _fetchPrices();
  }

  Future<void> _fetchPrices() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/price/administrador/prices'),
        headers: {'Authorization': 'Bearer ${widget.token}'},
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final List<dynamic> rawList = data['prices'] ?? [];
        _prices = rawList.map((e) => Price.fromJson(e)).toList();
      } else {
        _error = "Error al obtener precios (${response.statusCode})";
      }
    } catch (e) {
      _error = "Error de red: $e";
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  Widget _buildList() {
    if (_prices == null || _prices!.isEmpty) {
      return Center(child: Text("No hay precios registrados."));
    }
    return ListView.separated(
      itemCount: _prices!.length,
      separatorBuilder: (_, __) => Divider(),
      itemBuilder: (context, index) {
        final price = _prices![index];
        return ListTile(
          leading: CircleAvatar(
            child: Text(price.id.toString()),
          ),
          title: Text('Monto: \$${price.monto.toStringAsFixed(2)}'),
          subtitle: Text('ID Tipo Transporte: ${price.idTipoTransporte}'),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Lista de Tarifas'),
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: _loading ? null : _fetchPrices,
            tooltip: "Refrescar",
          ),
        ],
      ),
      body: _loading
          ? Center(child: CircularProgressIndicator())
          : _error != null
              ? Center(child: Text(_error!, style: TextStyle(color: Colors.red)))
              : _buildList(),
    );
  }
}