import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../config/config.dart';
import 'package:flutter/services.dart';

class PassengerPanel extends StatefulWidget {
  final String token;

  const PassengerPanel({Key? key, required this.token}) : super(key: key);

  @override
  State<PassengerPanel> createState() => _PassengerPanelState();
}

class _PassengerPanelState extends State<PassengerPanel> {
  String selectedSection = 'info';

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

  Future<List<dynamic>> fetchSchedules() async {
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/schedules/'),
      headers: {
        'Authorization': 'Bearer ${widget.token}',
        'accept': 'application/json',
      },
    );
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Error al cargar horarios');
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
      throw Exception('Error al cargar noticias y alertas');
    }
  }

  @override
  Widget build(BuildContext context) {
    // Define our color scheme
    const primaryColor = Color(0xFF1A73E8); // Blue
    const secondaryColor = Color(0xFF34A853); // Green accent
    const accentColor = Color(0xFFFBBC05); // Yellow accent
    const backgroundColor = Colors.white;
    const cardColor = Color(0xFFF8F9FA); // Light gray/white

    return Scaffold(
      appBar: AppBar(
        elevation: 0,
        backgroundColor: primaryColor,
        title: const Text(
          'Panel de Pasajero',
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
                        child: const Icon(Icons.person, color: Colors.white),
                      ),
                      const SizedBox(width: 12),
                      const Expanded(
                        child: Text(
                          'Pasajero',
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
                Expanded(
                  child: ListView(
                    padding: EdgeInsets.zero,
                    children: [
                      _buildMenuItem(
                        icon: Icons.info_outline,
                        title: 'Información general',
                        color: primaryColor,
                        isActive: selectedSection == 'info',
                        onTap: () {
                          setState(() {
                            selectedSection = 'info';
                          });
                        },
                      ),
                      _buildMenuItem(
                        icon: Icons.schedule_outlined,
                        title: 'Líneas, horarios y medios',
                        color: primaryColor,
                        isActive: selectedSection == 'schedules',
                        onTap: () {
                          setState(() {
                            selectedSection = 'schedules';
                          });
                        },
                      ),
                      _buildMenuItem(
                        icon: Icons.notifications_active_outlined,
                        title: 'Noticias y Alertas',
                        color: primaryColor,
                        isActive: selectedSection == 'incidences',
                        onTap: () {
                          setState(() {
                            selectedSection = 'incidences';
                          });
                        },
                      ),
                      // Los demás botones pueden agregarse igual si tienes los endpoints
                    ],
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
                child: _buildSectionContent(
                  selectedSection,
                  primaryColor,
                  secondaryColor,
                  accentColor,
                  cardColor,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSectionContent(
    String section,
    Color primaryColor,
    Color secondaryColor,
    Color accentColor,
    Color cardColor,
  ) {
    switch (section) {
      case 'schedules':
        return FutureBuilder<List<dynamic>>(
          future: fetchSchedules(),
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return _loadingWidget('Cargando horarios...');
            } else if (snapshot.hasError) {
              return _errorWidget('Error al cargar horarios');
            } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
              return _emptyWidget('No hay horarios disponibles.');
            }
            final schedules = snapshot.data!;
            return Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Líneas, horarios y medios',
                    style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                const SizedBox(height: 24),
                DataTable(
                  headingRowColor: MaterialStateProperty.all(
                      primaryColor.withOpacity(0.1)),
                  columns: const [
                    DataColumn(label: Text('ID')),
                    DataColumn(label: Text('Unidad')),
                    DataColumn(label: Text('Ruta')),
                    DataColumn(label: Text('Parada')),
                    DataColumn(label: Text('Llegada')),
                    DataColumn(label: Text('Salida')),
                  ],
                  rows: schedules.map((item) {
                    return DataRow(
                      cells: [
                        DataCell(Text(item['ID']?.toString() ?? '-')),
                        DataCell(Text(item['IDUnidad']?.toString() ?? '-')),
                        DataCell(Text(item['IDRuta']?.toString() ?? '-')),
                        DataCell(Text(item['IDParada']?.toString() ?? '-')),
                        DataCell(Text(item['Llegada']?.toString() ?? '-')),
                        DataCell(Text(item['Salida']?.toString() ?? '-')),
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
              return _loadingWidget('Cargando noticias y alertas...');
            } else if (snapshot.hasError) {
              return _errorWidget('Error al cargar noticias y alertas');
            } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
              return _emptyWidget('No hay noticias ni alertas.');
            }
            final incidences = snapshot.data!;
            return Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Noticias y Alertas',
                    style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                const SizedBox(height: 24),
                ...incidences.map((inc) => Card(
                      elevation: 0,
                      margin: const EdgeInsets.only(bottom: 16),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                        side: BorderSide(
                          color: accentColor.withOpacity(0.2),
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
                                Icon(Icons.announcement,
                                    color: accentColor, size: 22),
                                const SizedBox(width: 8),
                                Text(
                                  inc['Tipo']?.toString() ?? 'Alerta',
                                  style: const TextStyle(
                                    fontSize: 16,
                                    fontWeight: FontWeight.bold,
                                    color: Color(0xFF202124),
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 12),
                            Text(
                              inc['Descripcion']?.toString() ?? '',
                              style: const TextStyle(
                                fontSize: 15,
                                color: Color(0xFF202124),
                              ),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              'Unidad: ${inc['IDUnidad']?.toString() ?? '-'}',
                              style: const TextStyle(
                                fontSize: 13,
                                color: Color(0xFF5F6368),
                              ),
                            ),
                          ],
                        ),
                      ),
                    )),
              ],
            );
          },
        );
      default:
        // Información general
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
            final user = data['user'] ?? {};
            final typeCard = data['type_card'] ?? 'No disponible';
            final lastCardUse = data['ultimo_uso_tarjeta'] ?? {};
            final saldo = user['Saldo']?.toString() ?? '0.00';
            final lastTripDay = lastCardUse['day'] ?? 'N/A';
            final lastTripRoute = lastCardUse['route'] ?? 'N/A';
            final lastTripTime = lastCardUse['time'] ?? 'N/A';

            return Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Información general del pasajero',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF202124),
                  ),
                ),
                const SizedBox(height: 24),
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
                        _buildInfoRow(
                          'Nombre',
                          user['Nombre']?.toString() ?? 'No disponible',
                          Icons.badge_outlined,
                          primaryColor,
                        ),
                        _buildInfoRow(
                          'ID',
                          user['ID']?.toString() ?? 'No disponible',
                          Icons.credit_card_outlined,
                          primaryColor,
                        ),
                        _buildInfoRow(
                          'Correo',
                          user['Correo']?.toString() ?? 'No disponible',
                          Icons.email_outlined,
                          primaryColor,
                        ),
                        _buildInfoRow(
                          'Teléfono',
                          user['Telefono']?.toString() ?? 'No disponible',
                          Icons.phone_outlined,
                          primaryColor,
                        ),
                        _buildInfoRow(
                          'Tipo de tarjeta',
                          typeCard?.toString() ?? 'No disponible',
                          Icons.style_outlined,
                          secondaryColor,
                        ),
                        _buildInfoRow(
                          'Saldo disponible',
                          '\$$saldo',
                          Icons.account_balance_wallet_outlined,
                          secondaryColor,
                        ),
                        _buildInfoRow(
                          'Último viaje',
                          '$lastTripDay - $lastTripRoute - $lastTripTime',
                          Icons.history,
                          accentColor,
                        ),
                      ],
                    ),
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
      leading: Icon(icon, color: isActive ? color : const Color(0xFF5F6368)),
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
      onTap: onTap ?? () {},
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8),
      ),
      tileColor: isActive ? color.withOpacity(0.1) : null,
      hoverColor: color.withOpacity(0.05),
    );
  }

  Widget _buildInfoRow(
    String label,
    String value,
    IconData icon,
    Color iconColor,
  ) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(
            icon,
            size: 18,
            color: iconColor,
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  label,
                  style: const TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w500,
                    color: Color(0xFF5F6368),
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  value,
                  style: const TextStyle(
                    fontSize: 16,
                    color: Color(0xFF202124),
                  ),
                ),
              ],
            ),
          ),
        ],
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