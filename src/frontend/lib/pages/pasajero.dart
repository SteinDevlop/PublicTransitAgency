import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../config/config.dart';
import 'package:flutter/services.dart';

class PassengerPanel extends StatelessWidget {
  final String token;

  const PassengerPanel({Key? key, required this.token}) : super(key: key);

  Future<Map<String, dynamic>> fetchDashboardData(BuildContext context) async {
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
      body: FutureBuilder<Map<String, dynamic>>(
        future: fetchDashboardData(context),
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
                    'Cargando información...',
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
          final typeCard = data['type_card'] ?? 'No disponible';
          final lastCardUse = data['ultimo_uso_tarjeta'] ?? {};
          final saldo = user['Saldo']?.toString() ?? '0.00';

          // Ejemplo de último viaje (ajusta según tu backend)
          final lastTripDay = lastCardUse['day'] ?? 'N/A';
          final lastTripRoute = lastCardUse['route'] ?? 'N/A';
          final lastTripTime = lastCardUse['time'] ?? 'N/A';

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
                              user['Nombre']?.toString().substring(0, 1) ?? 'P',
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
                                  user['Nombre']?.toString() ?? 'Pasajero',
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
                                    color: secondaryColor,
                                    borderRadius: BorderRadius.circular(12),
                                  ),
                                  child: Text(
                                    'Saldo: \$$saldo',
                                    style: const TextStyle(
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
                            icon: Icons.map_outlined,
                            title: 'Planificador de viaje',
                            color: primaryColor,
                          ),
                          _buildMenuItem(
                            icon: Icons.schedule_outlined,
                            title: 'Líneas, horarios y medios',
                            color: primaryColor,
                          ),
                          _buildMenuItem(
                            icon: Icons.attach_money_outlined,
                            title: 'Tarifas y peajes',
                            color: primaryColor,
                          ),
                          _buildMenuItem(
                            icon: Icons.notifications_active_outlined,
                            title: 'Noticias y Alertas',
                            color: primaryColor,
                          ),
                          _buildMenuItem(
                            icon: Icons.history_outlined,
                            title: 'Movimientos',
                            color: primaryColor,
                          ),
                          _buildMenuItem(
                            icon: Icons.feedback_outlined,
                            title: 'Sugerencias y Quejas',
                            color: primaryColor,
                          ),
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
                    child: Column(
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
                              'Información general del pasajero',
                              style: TextStyle(
                                fontSize: 24,
                                fontWeight: FontWeight.bold,
                                color: Color(0xFF202124),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 24),
                        
                        // User Info Card
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
                                      Icons.person_outline,
                                      color: primaryColor,
                                      size: 22,
                                    ),
                                    const SizedBox(width: 8),
                                    const Text(
                                      'Datos Personales',
                                      style: TextStyle(
                                        fontSize: 18,
                                        fontWeight: FontWeight.bold,
                                        color: Color(0xFF202124),
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 16),
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
                              ],
                            ),
                          ),
                        ),
                        
                        const SizedBox(height: 20),
                        
                        // Card Info Card
                        Card(
                          elevation: 0,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(12),
                            side: BorderSide(
                              color: secondaryColor.withOpacity(0.1),
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
                                      Icons.credit_card,
                                      color: secondaryColor,
                                      size: 22,
                                    ),
                                    const SizedBox(width: 8),
                                    const Text(
                                      'Información de Tarjeta',
                                      style: TextStyle(
                                        fontSize: 18,
                                        fontWeight: FontWeight.bold,
                                        color: Color(0xFF202124),
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 16),
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
                              ],
                            ),
                          ),
                        ),
                        
                        const SizedBox(height: 20),
                        
                        // Last Trip Card
                        Card(
                          elevation: 0,
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
                                    Icon(
                                      Icons.history,
                                      color: accentColor,
                                      size: 22,
                                    ),
                                    const SizedBox(width: 8),
                                    const Text(
                                      'Último Viaje',
                                      style: TextStyle(
                                        fontSize: 18,
                                        fontWeight: FontWeight.bold,
                                        color: Color(0xFF202124),
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 16),
                                _buildInfoRow(
                                  'Día',
                                  lastTripDay,
                                  Icons.calendar_today_outlined,
                                  accentColor,
                                ),
                                _buildInfoRow(
                                  'Ruta',
                                  lastTripRoute,
                                  Icons.route_outlined,
                                  accentColor,
                                ),
                                _buildInfoRow(
                                  'Hora',
                                  lastTripTime,
                                  Icons.access_time_outlined,
                                  accentColor,
                                ),
                              ],
                            ),
                          ),
                        ),
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

  Widget _buildMenuItem({
    required IconData icon,
    required String title,
    required Color color,
  }) {
    return ListTile(
      leading: Icon(icon, color: color),
      title: Text(
        title,
        style: const TextStyle(
          fontSize: 14,
          fontWeight: FontWeight.w500,
          color: Color(0xFF202124),
        ),
      ),
      dense: true,
      horizontalTitleGap: 8,
      onTap: () {},
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8),
      ),
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
}