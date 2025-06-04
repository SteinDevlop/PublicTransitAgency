import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../config/config.dart';
import 'package:flutter/services.dart';
import 'dart:math';

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
          final lastCardUseRaw = data['ultimo_uso_tarjeta'];
          Map<String, dynamic> lastCardUse;
          if (lastCardUseRaw is Map) {
            lastCardUse = Map<String, dynamic>.from(lastCardUseRaw);
          } else if (lastCardUseRaw is String) {
            lastCardUse = {'tipo': lastCardUseRaw, 'monto': 'N/A'};
          } else {
            lastCardUse = {'tipo': 'N/A', 'monto': 'N/A'};
          }
          final lastCardType = lastCardUse['tipo']?.toString() ?? 'N/A';
          final lastCardMonto = lastCardUse['monto']?.toString() ?? 'N/A';

          final saldo = data['Saldo'] ?? '0.00';

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
                            onTap: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (_) =>
                                      PlanificadorViajeScreen(token: token),
                                ),
                              );
                            },
                          ),
                          _buildMenuItem(
                            icon: Icons.schedule_outlined,
                            title: 'Líneas, horarios y medios',
                            color: primaryColor,
                            onTap: () {
                              showDialog(
                                context: context,
                                builder: (_) => Dialog(
                                  child: Padding(
                                    padding: const EdgeInsets.all(24),
                                    child: SizedBox(
                                      width: 400,
                                      child: FutureBuilder<List<dynamic>>(
                                        future: _fetchHorarios(token),
                                        builder: (context, snapshot) {
                                          if (snapshot.connectionState ==
                                              ConnectionState.waiting) {
                                            return Center(
                                                child:
                                                    CircularProgressIndicator());
                                          } else if (snapshot.hasError) {
                                            return Center(
                                                child: Text(
                                                    'Error al cargar horarios'));
                                          } else if (!snapshot.hasData ||
                                              snapshot.data!.isEmpty) {
                                            return Center(
                                                child: Text(
                                                    'No hay horarios disponibles.'));
                                          }
                                          final horarios = snapshot.data!;
                                          return ListView.separated(
                                            shrinkWrap: true,
                                            itemCount: horarios.length,
                                            separatorBuilder: (_, __) =>
                                                Divider(),
                                            itemBuilder: (_, i) {
                                              final h = horarios[i];
                                              return ListTile(
                                                leading: Icon(Icons.access_time,
                                                    color: primaryColor),
                                                title: Text('ID: ${h['ID']}'),
                                                subtitle: Text(
                                                    'Llegada: ${h['Llegada']} | Salida: ${h['Salida']}'),
                                              );
                                            },
                                          );
                                        },
                                      ),
                                    ),
                                  ),
                                ),
                              );
                            },
                          ),
                          _buildMenuItem(
                            icon: Icons.attach_money_outlined,
                            title: 'Tarifas y peajes',
                            color: primaryColor,
                            onTap: () {
                              showDialog(
                                context: context,
                                builder: (_) => Dialog(
                                  child: SizedBox(
                                    width: 500,
                                    child: AdminPricesAndTypesWidget(token: token),
                                  ),
                                ),
                              );
                            },
                          ),
                          _buildMenuItem(
                            icon: Icons.notifications_active_outlined,
                            title: 'Noticias y Alertas',
                            color: primaryColor,
                            onTap: () {
                              showDialog(
                                context: context,
                                builder: (_) => Dialog(
                                  child: SizedBox(
                                    width: 500,
                                    child: IncidenciasPasajeroWidget(token: token),
                                  ),
                                ),
                              );
                            },
                          ),
                          _buildMenuItem(
                            icon: Icons.history_outlined,
                            title: 'Movimientos',
                            color: primaryColor,
                            onTap: () {
                              showDialog(
                                context: context,
                                builder: (_) => Dialog(
                                  child: SizedBox(
                                    width: 500,
                                    child: CardIdInputWidget(token: token),
                                  ),
                                ),
                              );
                            },
                          ),
                          _buildMenuItem(
                            icon: Icons.feedback_outlined,
                            title: 'Sugerencias y Quejas',
                            color: primaryColor,
                            onTap: () {
                              showDialog(
                                context: context,
                                builder: (_) => Dialog(
                                  child: PqrCrudWidget(token: token),
                                ),
                              );
                            },
                          ),
                          _buildMenuItem(
                            icon: Icons.payment_outlined,
                            title: 'Pago',
                            color: primaryColor,
                            onTap: () {
                              showDialog(
                                context: context,
                                builder: (_) => Dialog(
                                  child: PagoWidget(token: token, user: user),
                                ),
                              );
                            },
                          ),
                          _buildMenuItem(
                            icon: Icons.account_balance_wallet_outlined,
                            title: 'Recarga',
                            color: primaryColor,
                            onTap: () {
                              showDialog(
                                context: context,
                                builder: (_) => Dialog(
                                  child:
                                      RecargaWidget(token: token, user: user),
                                ),
                              );
                            },
                          ),
                          _buildMenuItem(
                            icon: Icons.alt_route,
                            title: 'Las rutas y sus paradas',
                            color: primaryColor,
                            onTap: () {
                              showDialog(
                                context: context,
                                builder: (_) => Dialog(
                                  child: SizedBox(
                                    width: 500,
                                    child: RutasParadasPasajeroWidget(token: token),
                                  ),
                                ),
                              );
                            },
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
                                  'Identificacion',
                                  user['Identificacion']?.toString() ??
                                      'No disponible',
                                  Icons.email_outlined,
                                  primaryColor,
                                ),
                                _buildInfoRow(
                                  'Correo',
                                  user['Correo']?.toString() ?? 'No disponible',
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
                                      'Último uso de tarjeta',
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
                                  'Tipo',
                                  lastCardType,
                                  Icons.credit_card,
                                  accentColor,
                                ),
                                _buildInfoRow(
                                  'Monto',
                                  lastCardMonto,
                                  Icons.attach_money,
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
    VoidCallback? onTap,
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
      onTap: onTap ?? () {},
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

  Future<List<dynamic>> _fetchHorarios(String token) async {
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/schedules/'),
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
}

class PlanificadorViajeScreen extends StatefulWidget {
  final String token;
  const PlanificadorViajeScreen({Key? key, required this.token})
      : super(key: key);

  @override
  State<PlanificadorViajeScreen> createState() =>
      _PlanificadorViajeScreenState();
}

class _PlanificadorViajeScreenState extends State<PlanificadorViajeScreen> {
  final TextEditingController _origenController = TextEditingController();
  final TextEditingController _destinoController = TextEditingController();
  bool _loading = false;
  String? _error;
  Map<String, dynamic>? _resultado;

  Future<void> _planificar() async {
    setState(() {
      _loading = true;
      _error = null;
      _resultado = null;
    });
    final origen = _origenController.text.trim();
    final destino = _destinoController.text.trim();
    if (origen.isEmpty || destino.isEmpty) {
      setState(() {
        _loading = false;
        _error = 'Completa ambos campos';
      });
      return;
    }
    try {
      final response = await http.post(
        Uri.parse('${AppConfig.baseUrl}/planificador/ubicaciones'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: {
          'ubicacion_entrada': origen,
          'ubicacion_final': destino,
        },
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          _resultado = data;
        });
      } else {
        setState(() {
          _error = 'No se encontró ruta o error en la consulta';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión';
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
        title: const Text('Planificador de Viaje'),
        backgroundColor: Color(0xFF1A73E8),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            TextField(
              controller: _origenController,
              decoration: InputDecoration(
                labelText: 'Ubicación inicial',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.location_on_outlined),
              ),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _destinoController,
              decoration: InputDecoration(
                labelText: 'Ubicación final',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.flag_outlined),
              ),
            ),
            const SizedBox(height: 20),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _loading ? null : _planificar,
                child: _loading
                    ? SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(
                            strokeWidth: 2, color: Colors.white),
                      )
                    : Text('Planificar viaje'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Color(0xFF1A73E8),
                  foregroundColor: Colors.white,
                  padding: EdgeInsets.symmetric(vertical: 14),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ),
            ),
            if (_error != null) ...[
              const SizedBox(height: 16),
              Text(_error!, style: TextStyle(color: Colors.red)),
            ],
            if (_resultado != null) ...[
              const SizedBox(height: 32),
              Card(
                elevation: 4,
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
                          Icon(Icons.alt_route,
                              color: Color(0xFF1A73E8), size: 32),
                          const SizedBox(width: 12),
                          const Text('Resultado de Planificación',
                              style: TextStyle(
                                  fontSize: 20, fontWeight: FontWeight.bold)),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ],
            // Mostrar solo si hay interconexiones (lista)
            if (_resultado != null &&
                _resultado!['interconexiones'] != null &&
                (_resultado!['interconexiones'] as List).isNotEmpty) ...[
              const SizedBox(height: 32),
              ...(_resultado!['interconexiones'] as List)
                  .map<Widget>((item) => Card(
                        elevation: 4,
                        margin: const EdgeInsets.only(bottom: 20),
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
                                  Icon(Icons.alt_route,
                                      color: Color(0xFF1A73E8), size: 32),
                                  const SizedBox(width: 12),
                                  const Text('Interconexión',
                                      style: TextStyle(
                                          fontSize: 20,
                                          fontWeight: FontWeight.bold)),
                                ],
                              ),
                              const SizedBox(height: 20),
                              _buildResultRow('Ruta Inicial',
                                  item['ruta_inicio']?.toString() ?? '-'),
                              _buildResultRow('Interconexión',
                                  item['interconexion']?.toString() ?? '-'),
                              _buildResultRow('Ruta Final',
                                  item['ruta_final']?.toString() ?? '-'),
                            ],
                          ),
                        ),
                      ))
                  .toList(),
            ]
            // Si no hay interconexiones pero sí resultado plano
            else if (_resultado != null &&
                _resultado!['ruta_inicial'] != null) ...[
              const SizedBox(height: 32),
              Card(
                elevation: 4,
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
                          Icon(Icons.alt_route,
                              color: Color(0xFF1A73E8), size: 32),
                          const SizedBox(width: 12),
                          const Text('Resultado de Planificación',
                              style: TextStyle(
                                  fontSize: 20, fontWeight: FontWeight.bold)),
                        ],
                      ),
                      const SizedBox(height: 20),
                      _buildResultRow('Ruta Inicial',
                          _resultado!['ruta_inicial']?.toString() ?? '-'),
                      _buildResultRow('Interconexión',
                          _resultado!['interconexion']?.toString() ?? '-'),
                      _buildResultRow('Ruta Final',
                          _resultado!['ruta_final']?.toString() ?? '-'),
                    ],
                  ),
                ),
              ),
            ]
            // Si no hay nada útil
            else if (_resultado != null) ...[
              const SizedBox(height: 32),
              Text('No se encontraron rutas para la búsqueda.',
                  style: TextStyle(color: Colors.red)),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildResultRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6.0),
      child: Row(
        children: [
          Text('$label:', style: TextStyle(fontWeight: FontWeight.bold)),
          const SizedBox(width: 8),
          Expanded(child: Text(value, style: TextStyle(fontSize: 16))),
        ],
      ),
    );
  }
}

class PagoWidget extends StatefulWidget {
  final String token;
  final Map<String, dynamic> user;
  const PagoWidget({Key? key, required this.token, required this.user})
      : super(key: key);
  @override
  State<PagoWidget> createState() => _PagoWidgetState();
}

class _PagoWidgetState extends State<PagoWidget> {
  final _formKey = GlobalKey<FormState>();
  int? _selectedTransportId;
  double? _selectedMonto;
  int? _selectedTipoTransporte;
  int? _selectedUnidadId;
  bool _loading = false;
  String? _error;
  Map<String, dynamic>? _detallePago;
  List<Map<String, dynamic>> _transportOptions = [];
  List<Map<String, dynamic>> _unidadesOptions = [];
  double saldoActual = 0.0;

  @override
  void initState() {
    super.initState();
    _initSaldo();
    _fetchTransportOptions();
  }

  Future<void> _initSaldo() async {
    saldoActual = await _obtenerSaldoDashboard(widget.token);
    if (mounted) setState(() {});
  }

  Future<double> _obtenerSaldoDashboard(String token) async {
    final url = '${AppConfig.baseUrl}/login/dashboard';
    print('DEBUG: URL solicitada = $url');
    print('DEBUG: Token enviado: $token');

    try {
      final response = await http.get(
        Uri.parse(url),
        headers: {
          'Authorization': 'Bearer $token',
          'accept': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final rawBody = response.body.replaceAll('None', 'null');
        print('DEBUG: rawBody modificado = $rawBody');

        final data = json.decode(rawBody);
        print('DEBUG: data = $data');

        if (data.containsKey('Saldo') && data['Saldo'] != null) {
          final saldo = data['Saldo'];

          final saldoConvertido = (saldo is int)
              ? saldo.toDouble()
              : (saldo is double)
                  ? saldo
                  : (saldo is String)
                      ? double.tryParse(saldo) ?? 0.0
                      : 0.0;

          print('DEBUG: Saldo retornado = $saldoConvertido');
          return saldoConvertido;
        } else {
          print('DEBUG: El campo "Saldo" es null o no existe en el dashboard');
          throw Exception('Campo "Saldo" no válido en dashboard');
        }
      } else {
        print(
            'Error en la respuesta: ${response.statusCode} - ${response.body}');
        throw Exception('Error al consultar dashboard');
      }
    } catch (e) {
      print('ERROR: al obtener el saldo del dashboard: $e');
      throw Exception('Error de conexión o datos');
    }
  }

  Future<void> _fetchTransportOptions() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      debugPrint('[PagoWidget] Solicitando precios...');
      final pricesResp = await http.get(
        Uri.parse('${AppConfig.baseUrl}/price/pasajero/prices'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json'
        },
      );
      debugPrint(
          '[PagoWidget] Respuesta precios: statusCode=${pricesResp.statusCode}');
      debugPrint('[PagoWidget] Solicitando tipos de transporte...');
      final transportsResp = await http.get(
        Uri.parse('${AppConfig.baseUrl}/typetransport/typetransports'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json'
        },
      );
      debugPrint(
          '[PagoWidget] Respuesta tipos de transporte: statusCode=${transportsResp.statusCode}');
      if (pricesResp.statusCode == 200 && transportsResp.statusCode == 200) {
        final pricesDecoded = json.decode(pricesResp.body);
        final transportsDecoded = json.decode(transportsResp.body);
        // Extraer listas reales si vienen envueltas en un objeto
        final pricesList = (pricesDecoded is List)
            ? pricesDecoded
            : (pricesDecoded is Map && pricesDecoded.containsKey('prices'))
                ? pricesDecoded['prices']
                : [];
        final transportsList = (transportsDecoded is List)
            ? transportsDecoded
            : (transportsDecoded is Map &&
                    transportsDecoded.containsKey('typetransports'))
                ? transportsDecoded['typetransports']
                : [];
        if (pricesList is! List || transportsList is! List) {
          debugPrint(
              '[PagoWidget] Error: precios o transportes no son listas.');
          debugPrint(
              '[PagoWidget] pricesDecoded: \\${pricesDecoded.toString()}');
          debugPrint(
              '[PagoWidget] transportsDecoded: \\${transportsDecoded.toString()}');
          if (mounted) {
            setState(() {
              _error =
                  'Error: precios o transportes no son listas.\nPrecios: \\${pricesDecoded.toString()}\nTransportes: \\${transportsDecoded.toString()}';
            });
          }
          return;
        }
        final prices = List<Map<String, dynamic>>.from(pricesList.map((e) =>
            e is Map<String, dynamic>
                ? e
                : Map<String, dynamic>.from(e as Map)));
        final transports = List<Map<String, dynamic>>.from(transportsList.map(
            (e) => e is Map<String, dynamic>
                ? e
                : Map<String, dynamic>.from(e as Map)));
        debugPrint('[PagoWidget] Precios obtenidos: \\${prices.length}');
        debugPrint(
            '[PagoWidget] Transportes obtenidos: \\${transports.length}');
        // Cruzar precios y transportes
        final options = <Map<String, dynamic>>[];
        for (final price in prices) {
          final tipoId = price['IDTipoTransporte'];
          final monto = price['Monto'];
          final transport = transports.firstWhere(
            (t) => t['ID'] == tipoId,
            orElse: () => <String, dynamic>{},
          );
          if (transport.isNotEmpty) {
            options.add({
              'IDTipoTransporte': tipoId,
              'Monto': monto,
              'Nombre': transport['TipoTransporte'] ?? transport['Transporte'],
              'ID': transport['ID'],
            });
          } else {
            debugPrint(
                '[PagoWidget] No se encontró transporte para IDTipoTransporte=$tipoId');
          }
        }
        if (mounted) {
          setState(() {
            _transportOptions = options;
          });
        }
      } else {
        debugPrint(
            '[PagoWidget] Error al cargar transportes o precios. Status precios: \\${pricesResp.statusCode}, Status transportes: \\${transportsResp.statusCode}');
        if (mounted) {
          setState(() {
            _error = 'Error al cargar transportes o precios.';
          });
        }
      }
    } catch (e) {
      debugPrint(
          '[PagoWidget] Error de conexión al cargar transportes: \\${e.toString()}');
      if (mounted) {
        setState(() {
          _error = 'Error de conexión al cargar transportes.';
        });
      }
    } finally {
      if (mounted) {
        setState(() {
          _loading = false;
        });
      }
    }
  }

  Future<void> _fetchUnidadesForTipo(int tipoId) async {
    if (!mounted) return;
    setState(() {
      _loading = true;
      _error = null;
      _unidadesOptions = [];
      _selectedUnidadId = null;
    });
    try {
      final resp = await http.get(
        Uri.parse('${AppConfig.baseUrl}/transport_units/'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json'
        },
      );
      if (resp.statusCode == 200) {
        final decoded = json.decode(resp.body);
        final unidadesList = (decoded is Map && decoded.containsKey('data'))
            ? decoded['data']
            : (decoded is List ? decoded : []);
        final filtradas = unidadesList.where((u) {
          final idTipo = u['IDTipo'];
          int? idTipoInt;
          if (idTipo is int) {
            idTipoInt = idTipo;
          } else if (idTipo is String) {
            idTipoInt = int.tryParse(idTipo);
          }
          // Excluir IDTipo == 0 (None) y también excluir si el nombre es 'None'
          final nombre =
              (u['Nombre'] ?? u['Ubicacion'] ?? '').toString().toLowerCase();
          return idTipoInt != null &&
              idTipoInt != 0 &&
              nombre != 'none' &&
              idTipoInt == tipoId;
        }).toList();
        debugPrint(
            '[PagoWidget] Unidades filtradas para tipo $tipoId: ${filtradas.length}');
        setState(() {
          _unidadesOptions = List<Map<String, dynamic>>.from(filtradas);
        });
      } else {
        debugPrint(
            '[PagoWidget] Error al cargar unidades: statusCode=${resp.statusCode}, body=${resp.body}');
        if (mounted) {
          setState(() {
            _error = 'Error al cargar unidades de transporte.';
          });
        }
      }
    } catch (e) {
      debugPrint('[PagoWidget] Error de conexión al cargar unidades: $e');
      if (mounted) {
        setState(() {
          _error = 'Error de conexión al cargar unidades.';
        });
      }
    } finally {
      if (mounted) {
        setState(() {
          _loading = false;
        });
      }
    }
  }

  Future<void> _realizarPago() async {
    if (!_formKey.currentState!.validate() ||
        _selectedTransportId == null ||
        _selectedUnidadId == null) return;
    // saldoActual ya está inicializado en initState y se puede usar aquí
    debugPrint('[PagoWidget] Saldo detectado: $saldoActual');
    final montoPago = _selectedMonto ?? 0.0;
    if (saldoActual - montoPago < 0) {
      debugPrint(
          '[PagoError] Es insuficiente debido a que saldo - monto es: $saldoActual - $montoPago');
      setState(() {
        _error = 'Saldo insuficiente para realizar el pago.';
      });
      return;
    }
    setState(() {
      _loading = true;
      _error = null;
      _detallePago = null;
    });
    final random = Random();
    final idPago = (100 + random.nextInt(2147483547 - 100)).toString();
    final idMovimiento = (100 + random.nextInt(2147483547 - 100)).toString();
    final idTarjeta = widget.user['IDTarjeta']?.toString() ?? '';
    try {
      // 1. POST /movement/create
      final movResp = await http.post(
        Uri.parse('${AppConfig.baseUrl}/movement/create'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: {
          'ID': idMovimiento,
          'IDTipoMovimiento': '1',
          'Monto': _selectedMonto.toString(),
          'IDTarjeta': idTarjeta.toString()
        },
      );
      if (movResp.statusCode != 201 && movResp.statusCode != 200) {
        setState(() {
          _error = 'Error al crear movimiento: ${movResp.body}';
          _loading = false;
        });
        return;
      }
      // 2. POST /payments/create
      final payBody = {
        'IDMovimiento': idMovimiento,
        'IDPago': idPago,
        'IDTarjeta': idTarjeta,
        'IDPrecio': _selectedTransportId?.toString() ?? '',
        'IDUnidad': _selectedUnidadId?.toString() ?? '',
        'ID': idPago, // ID es el IDPago generado
      };
      debugPrint(
          '[PagoWidget] Body para /payments/create: ' + payBody.toString());
      final payResp = await http.post(
        Uri.parse('${AppConfig.baseUrl}/payments/create'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: payBody,
      );
      if (payResp.statusCode != 200 && payResp.statusCode != 201) {
        setState(() {
          _error = 'Error al crear pago: ${payResp.body}';
          _loading = false;
        });
        return;
      }
      // 3. GET /payments/{IDPago}
      final detResp = await http.get(
        Uri.parse('${AppConfig.baseUrl}/payments/$idPago'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json'
        },
      );
      if (detResp.statusCode == 200) {
        setState(() {
          _detallePago = json.decode(detResp.body);
        });
      } else {
        setState(() {
          _error = 'Pago realizado, pero no se pudo obtener el detalle.';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión al realizar el pago.';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final primaryColor = const Color(0xFF1A73E8);
    final secondaryColor = const Color(0xFF34A853);
    final cardColor = const Color(0xFFF8F9FA);
    return SizedBox(
      width: 420,
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Card(
          elevation: 0,
          color: cardColor,
          shape:
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: _loading
                ? Center(child: CircularProgressIndicator(color: primaryColor))
                : _detallePago != null
                    ? _buildDetallePago(
                        _detallePago!, primaryColor, secondaryColor)
                    : SingleChildScrollView(
                        child: Form(
                          key: _formKey,
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(
                                children: [
                                  Icon(Icons.payment_outlined,
                                      color: primaryColor, size: 28),
                                  const SizedBox(width: 10),
                                  const Text('Realizar Pago',
                                      style: TextStyle(
                                          fontWeight: FontWeight.bold,
                                          fontSize: 22,
                                          color: Color(0xFF202124))),
                                ],
                              ),
                              const SizedBox(height: 20),
                              DropdownButtonFormField<int>(
                                decoration: InputDecoration(
                                  labelText: 'Tipo de Transporte',
                                  border: OutlineInputBorder(),
                                  prefixIcon: Icon(Icons.directions_transit,
                                      color: primaryColor),
                                ),
                                items: _transportOptions
                                    .map((opt) => DropdownMenuItem<int>(
                                          value: opt['IDTipoTransporte'],
                                          child: Text(
                                              '${opt['Nombre']} (${opt['Monto']})'),
                                        ))
                                    .toList(),
                                onChanged: (val) {
                                  final selected = _transportOptions.firstWhere(
                                      (opt) => opt['IDTipoTransporte'] == val);
                                  setState(() {
                                    _selectedTransportId = selected['ID'];
                                    _selectedMonto = selected['Monto'] is int
                                        ? (selected['Monto'] as int).toDouble()
                                        : selected['Monto'];
                                    _selectedTipoTransporte =
                                        selected['IDTipoTransporte'];
                                    _unidadesOptions = [];
                                    _selectedUnidadId = null;
                                  });
                                  if (val != null) _fetchUnidadesForTipo(val);
                                },
                                value: _selectedTipoTransporte,
                                validator: (v) => v == null
                                    ? 'Seleccione un tipo de transporte'
                                    : null,
                              ),
                              const SizedBox(height: 16),
                              if (_unidadesOptions.isNotEmpty)
                                DropdownButtonFormField<int>(
                                  decoration: InputDecoration(
                                    labelText: 'Unidad de Transporte',
                                    border: OutlineInputBorder(),
                                    prefixIcon: Icon(Icons.directions_bus,
                                        color: primaryColor),
                                  ),
                                  items: _unidadesOptions
                                      .map((u) => DropdownMenuItem<int>(
                                            value: u['ID'] is int
                                                ? u['ID']
                                                : int.tryParse(
                                                    u['ID'].toString()),
                                            child: Text(u['Nombre'] ??
                                                u['ID'].toString()),
                                          ))
                                      .toList(),
                                  onChanged: (val) {
                                    setState(() {
                                      _selectedUnidadId = val;
                                    });
                                  },
                                  validator: (v) => v == null
                                      ? 'Seleccione una unidad'
                                      : null,
                                ),
                              const SizedBox(height: 24),
                              SizedBox(
                                width: double.infinity,
                                child: ElevatedButton(
                                  onPressed: _loading ? null : _realizarPago,
                                  child: const Text('Enviar',
                                      style: TextStyle(fontSize: 16)),
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: primaryColor,
                                    foregroundColor: Colors.white,
                                    padding: const EdgeInsets.symmetric(
                                        vertical: 14),
                                    shape: RoundedRectangleBorder(
                                        borderRadius:
                                            BorderRadius.circular(12)),
                                  ),
                                ),
                              ),
                              if (_error != null) ...[
                                const SizedBox(height: 16),
                                Text(_error!,
                                    style: const TextStyle(color: Colors.red)),
                              ],
                            ],
                          ),
                        ),
                      ),
          ),
        ),
      ));
  }

  Widget _buildDetallePago(
      Map<String, dynamic> pago, Color primaryColor, Color secondaryColor) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(Icons.check_circle, color: secondaryColor, size: 28),
            const SizedBox(width: 10),
            const Text('Pago realizado con éxito',
                style: TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 20,
                    color: Color(0xFF202124))),
          ],
        ),
        const SizedBox(height: 16),
        ...pago.entries.map((e) => Padding(
              padding: const EdgeInsets.symmetric(vertical: 4),
              child: Row(
                children: [
                  Text('${e.key}: ',
                      style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          color: Color(0xFF5F6368))),
                  Expanded(
                      child: Text(e.value.toString(),
                          style: const TextStyle(fontSize: 16))),
                ],
              ),
            )),
        const SizedBox(height: 20),
        SizedBox(
          width: double.infinity,
          child: ElevatedButton(
            onPressed: () {
              Navigator.of(context).pop();
              // Recarga la página para actualizar el dashboard
              Navigator.of(context).pushReplacement(
                MaterialPageRoute(
                  builder: (context) => PassengerPanel(token: widget.token),
                ),
              );
            },
            child: const Text('Cerrar'),
            style: ElevatedButton.styleFrom(backgroundColor: secondaryColor),
          ),
        ),
      ],
    );
  }
}

class RecargaWidget extends StatefulWidget {
  final String token;
  final Map<String, dynamic> user;
  const RecargaWidget({Key? key, required this.token, required this.user})
      : super(key: key);
  @override
  State<RecargaWidget> createState() => _RecargaWidgetState();
}

class _RecargaWidgetState extends State<RecargaWidget> {
  final _formKey = GlobalKey<FormState>();
  final _montoController = TextEditingController();
  bool _loading = false;
  String? _error;
  Map<String, dynamic>? _detalleRecarga;
  bool _confirmar = false;

  Future<void> _realizarRecarga() async {
    final montoStr = _montoController.text.trim();
    final monto = double.tryParse(montoStr);
    if (monto == null || monto <= 0 || monto > 100000) {
      setState(() {
        _error = 'El monto debe ser mayor a 0 y menor o igual a 100000.';
      });
      return;
    }
    setState(() {
      _loading = true;
      _error = null;
      _detalleRecarga = null;
    });
    final random = Random();
    String nuevoId = '';
    try {
      // 2. Obtener nuevo ID de movimiento
      final movIdResp = await http.get(
        Uri.parse('${AppConfig.baseUrl}/movement/administrador/crear'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json'
        },
      );
      debugPrint(
          '[RecargaWidget] movIdResp: statusCode=${movIdResp.statusCode}, body=${movIdResp.body}');
      if (movIdResp.statusCode != 200) {
        setState(() {
          _error = 'Error al generar ID de movimiento.';
          _loading = false;
        });
        return;
      }
      nuevoId = json.decode(movIdResp.body)['nuevo_id'].toString();
      final idTarjeta = widget.user['IDTarjeta'] is int
          ? widget.user['IDTarjeta']
          : int.tryParse(widget.user['IDTarjeta']?.toString() ?? '0') ?? 0;
      // 3. POST /movement/create
      final movResp = await http.post(
        Uri.parse('${AppConfig.baseUrl}/movement/create'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: {
          'ID': nuevoId,
          'IDTipoMovimiento': '2',
          'Monto': montoStr,
          'IDTarjeta': idTarjeta.toString()
        },
      );
      debugPrint(
          '[RecargaWidget] movResp: statusCode=${movResp.statusCode}, body=${movResp.body}');
      if (movResp.statusCode != 201 && movResp.statusCode != 200) {
        setState(() {
          _error = 'Error al crear movimiento: ${movResp.body}';
          _loading = false;
        });
        return;
      }
      // 4. POST /payments/create
      final idPago = (100 + random.nextInt(2147483547 - 100)).toString();
      final payBody = {
        'IDMovimiento': nuevoId.toString(),
        'IDPrecio': '0',
        'IDTarjeta': idTarjeta.toString(),
        'IDUnidad': '0',
        'ID': idPago.toString(),
      };
      debugPrint(
          '[RecargaWidget] Body para /payments/create: ' + payBody.toString());
      final payResp = await http.post(
        Uri.parse('${AppConfig.baseUrl}/payments/create'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: payBody,
      );
      debugPrint(
          '[RecargaWidget] payResp: statusCode=${payResp.statusCode}, body=${payResp.body}');
      if (payResp.statusCode != 200 && payResp.statusCode != 201) {
        setState(() {
          _error = 'Error al crear recarga: ${payResp.body}';
          _loading = false;
        });
        return;
      }
      // 5. GET /payments/{IDPago}
      final detResp = await http.get(
        Uri.parse('${AppConfig.baseUrl}/payments/$idPago'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json'
        },
      );
      debugPrint(
          '[RecargaWidget] detResp: statusCode=${detResp.statusCode}, body=${detResp.body}');
      if (detResp.statusCode == 200) {
        setState(() {
          _detalleRecarga = json.decode(detResp.body);
        });
      } else {
        setState(() {
          _error = 'Recarga realizada, pero no se pudo obtener el detalle.';
        });
      }
    } catch (e, st) {
      debugPrint('[RecargaWidget] EXCEPCION: $e\n$st');
      setState(() {
        _error = 'Error de conexión al realizar la recarga.';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final primaryColor = const Color(0xFF1A73E8);
    final secondaryColor = const Color(0xFF34A853);
    final cardColor = const Color(0xFFF8F9FA);
    return SizedBox(
      width: 420,
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Card(
          elevation: 0,
          color: cardColor,
          shape:
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: _loading
                ? Center(child: CircularProgressIndicator(color: primaryColor))
                : _detalleRecarga != null
                    ? _buildDetalleRecarga(
                        _detalleRecarga!, primaryColor, secondaryColor)
                    : SingleChildScrollView(
                        child: Form(
                          key: _formKey,
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(
                                children: [
                                  Icon(Icons.account_balance_wallet_outlined,
                                      color: primaryColor, size: 28),
                                  const SizedBox(width: 10),
                                  const Text('Recargar Tarjeta',
                                      style: TextStyle(
                                          fontWeight: FontWeight.bold,
                                          fontSize: 22,
                                          color: Color(0xFF202124))),
                                ],
                              ),
                              const SizedBox(height: 20),
                              TextFormField(
                                controller: _montoController,
                                keyboardType: TextInputType.number,
                                decoration: InputDecoration(
                                  labelText: 'Monto',
                                  border: OutlineInputBorder(),
                                  prefixIcon: Icon(Icons.attach_money,
                                      color: primaryColor),
                                ),
                                validator: (v) {
                                  final val = double.tryParse(v ?? '');
                                  if (val == null || val <= 0 || val > 100000) {
                                    return 'El monto debe ser mayor a 0 y menor o igual a 100000.';
                                  }
                                  return null;
                                },
                              ),
                              const SizedBox(height: 24),
                              if (!_confirmar)
                                SizedBox(
                                  width: double.infinity,
                                  child: ElevatedButton(
                                    onPressed: _loading
                                        ? null
                                        : () {
                                            if (_formKey.currentState!
                                                .validate()) {
                                              setState(() {
                                                _confirmar = true;
                                              });
                                            }
                                          },
                                    child: const Text('Confirmar recarga',
                                        style: TextStyle(fontSize: 16)),
                                    style: ElevatedButton.styleFrom(
                                      backgroundColor: primaryColor,
                                      foregroundColor: Colors.white,
                                      padding: const EdgeInsets.symmetric(
                                          vertical: 14),
                                      shape: RoundedRectangleBorder(
                                          borderRadius:
                                              BorderRadius.circular(12)),
                                    ),
                                  ),
                                ),
                              if (_confirmar) ...[
                                Text(
                                    '¿Confirmar recarga de \\${_montoController.text}?',
                                    style: const TextStyle(
                                        color: Color(0xFF1A73E8),
                                        fontWeight: FontWeight.bold)),
                                const SizedBox(height: 12),
                                SizedBox(
                                  width: double.infinity,
                                  child: ElevatedButton(
                                    onPressed:
                                        _loading ? null : _realizarRecarga,
                                    child: const Text('Recargar',
                                        style: TextStyle(fontSize: 16)),
                                    style: ElevatedButton.styleFrom(
                                        backgroundColor: secondaryColor,
                                        foregroundColor: Colors.white),
                                  ),
                                ),
                                const SizedBox(height: 8),
                                TextButton(
                                  onPressed: () {
                                    setState(() {
                                      _confirmar = false;
                                    });
                                  },
                                  child: const Text('Cancelar'),
                                ),
                              ],
                              if (_error != null) ...[
                                const SizedBox(height: 16),
                                Text(_error!,
                                    style: const TextStyle(color: Colors.red)),
                              ],
                            ],
                          ),
                        ),
                      ),
          ),
        ),
      ));
  }

  Widget _buildDetalleRecarga(
      Map<String, dynamic> pago, Color primaryColor, Color secondaryColor) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(Icons.check_circle, color: secondaryColor, size: 28),
            const SizedBox(width: 10),
            const Text('Recarga realizada con éxito',
                style: TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 20,
                    color: Color(0xFF202124))),
          ],
        ),
        const SizedBox(height: 16),
        ...pago.entries.map((e) => Padding(
              padding: const EdgeInsets.symmetric(vertical: 4),
              child: Row(
                children: [
                  Text('${e.key}: ',
                      style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          color: Color(0xFF5F6368))),
                  Expanded(
                      child: Text(e.value.toString(),
                          style: const TextStyle(fontSize: 16))),
                ],
              ),
            )),
        const SizedBox(height: 20),
        SizedBox(
          width: double.infinity,
          child: ElevatedButton(
            onPressed: () {
              Navigator.of(context).pop();
              // Recarga la página para actualizar el dashboard
              Navigator.of(context).pushReplacement(
                MaterialPageRoute(
                  builder: (context) => PassengerPanel(token: widget.token),
                ),
              );
            },
            child: const Text('Cerrar'),
            style: ElevatedButton.styleFrom(backgroundColor: secondaryColor),
          ),
        ),
      ],
    );
  }
}

class IncidenciasPasajeroWidget extends StatefulWidget {
  final String token;
  const IncidenciasPasajeroWidget({Key? key, required this.token}) : super(key: key);

  @override
  State<IncidenciasPasajeroWidget> createState() => _IncidenciasPasajeroWidgetState();
}

class _IncidenciasPasajeroWidgetState extends State<IncidenciasPasajeroWidget> {
  bool _loading = true;
  String? _error;
  List<dynamic> _incidencias = [];

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
        Uri.parse('${AppConfig.baseUrl}/incidences/'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
        },
      );
      if (response.statusCode == 200) {
        setState(() {
          _incidencias = json.decode(response.body);
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

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text('Noticias y Alertas', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20)),
          const SizedBox(height: 16),
          if (_loading)
            Center(child: CircularProgressIndicator())
          else if (_error != null)
            Text(_error!, style: TextStyle(color: Colors.red))
          else if (_incidencias.isEmpty)
            Text('No hay incidencias registradas.')
          else
            Expanded(
              child: ListView.separated(
                shrinkWrap: true,
                itemCount: _incidencias.length,
                separatorBuilder: (_, __) => Divider(),
                itemBuilder: (context, i) {
                  final inc = _incidencias[i];
                  return ListTile(
                    leading: Icon(Icons.warning_amber_rounded, color: Colors.orange),
                    title: Text(inc['Descripcion'] ?? 'Sin descripción'),
                    subtitle: Text('Tipo: ${inc['Tipo'] ?? '-'} | Unidad: ${inc['IDUnidad'] ?? '-'}'),
                  );
                },
              ),
            ),
        ],
      ),
    );
  }
}

class RutasParadasPasajeroWidget extends StatefulWidget {
  final String token;
  const RutasParadasPasajeroWidget({Key? key, required this.token}) : super(key: key);

  @override
  State<RutasParadasPasajeroWidget> createState() => _RutasParadasPasajeroWidgetState();
}

class _RutasParadasPasajeroWidgetState extends State<RutasParadasPasajeroWidget> {
  bool _loading = true;
  String? _error;
  List<dynamic> _relaciones = [];

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

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text('Rutas y sus Paradas', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20)),
          const SizedBox(height: 16),
          if (_loading)
            Center(child: CircularProgressIndicator())
          else if (_error != null)
            Text(_error!, style: TextStyle(color: Colors.red))
          else if (_relaciones.isEmpty)
            Text('No hay relaciones registradas.')
          else
            Expanded(
              child: ListView.separated(
                shrinkWrap: true,
                itemCount: _relaciones.length,
                separatorBuilder: (_, __) => Divider(),
                itemBuilder: (context, i) {
                  final rel = _relaciones[i];
                  return ListTile(
                    leading: Icon(Icons.directions_bus, color: Colors.blue),
                    title: Text('Ruta: ${rel['NombreRuta'] ?? '-'}'),
                    subtitle: Text('Parada: ${rel['NombreParada'] ?? '-'}'),
                  );
                },
              ),
            ),
        ],
      ),
    );
  }
}
///
// Modelo para el precio
class Price {
  final int id;
  final int idTipoTransporte;
  final double monto;

  Price({
    required this.id,
    required this.idTipoTransporte,
    required this.monto,
  });

  factory Price.fromJson(Map<String, dynamic> json) => Price(
        id: json['ID'],
        idTipoTransporte: json['IDTipoTransporte'],
        monto: (json['Monto'] is int)
            ? (json['Monto'] as int).toDouble()
            : (json['Monto'] as double),
      );
}

// Modelo para el tipo de transporte
class TypeTransport {
  final int id;
  final String nombre;

  TypeTransport({required this.id, required this.nombre});

  factory TypeTransport.fromJson(Map<String, dynamic> json) => TypeTransport(
        id: json['ID'],
        nombre: json['TipoTransporte'],
      );
}

class AdminPricesAndTypesWidget extends StatefulWidget {
  final String token;

  const AdminPricesAndTypesWidget({
    Key? key,
    required this.token,
  }) : super(key: key);

  @override
  State<AdminPricesAndTypesWidget> createState() => _AdminPricesAndTypesWidgetState();
}

class _AdminPricesAndTypesWidgetState extends State<AdminPricesAndTypesWidget> {
  List<Price>? _prices;
  List<TypeTransport>? _types;
  bool _loading = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    _fetchAll();
  }

  void _setLoading(bool value) {
    setState(() {
      _loading = value;
    });
  }

  void _showMessage(String msg, {bool isError = false}) {
    setState(() {
      _error = msg;
    });
  }

  Future<void> _fetchAll() async {
    _setLoading(true);
    _error = null;

    try {
      // Consultar precios
      final responsePrecios = await http.get(
        Uri.parse('${AppConfig.baseUrl}/price/pasajero/prices'),
        headers: {'Authorization': 'Bearer ${widget.token}'},
      );
      if (responsePrecios.statusCode == 200) {
        final List<dynamic> data = json.decode(responsePrecios.body)['prices'];
        _prices = data.map((e) => Price.fromJson(e)).toList();
      } else {
        _showMessage("Error al consultar precios: ${responsePrecios.body}", isError: true);
        _setLoading(false);
        return;
      }

      // Consultar tipos de transporte
      final responseTipos = await http.get(
        Uri.parse('${AppConfig.baseUrl}/typetransport/typetransports'),
        headers: {'Authorization': 'Bearer ${widget.token}'},
      );
      if (responseTipos.statusCode == 200) {
        final List<dynamic> data = json.decode(responseTipos.body)['typetransports'];
        _types = data.map((e) => TypeTransport.fromJson(e)).toList();
      } else {
        _showMessage("Error al consultar tipos de transporte: ${responseTipos.body}", isError: true);
      }
    } catch (e) {
      _showMessage("Error de conexión: $e", isError: true);
    } finally {
      _setLoading(false);
    }
  }

  Widget _buildPricesTable() {
    if (_prices == null || _prices!.isEmpty) {
      return Center(child: Text("No hay precios registrados."));
    }
    return DataTable(
      columns: const [
        DataColumn(label: Text("ID")),
        DataColumn(label: Text("ID Tipo Transporte")),
        DataColumn(label: Text("Monto")),
      ],
      rows: _prices!
          .map(
            (price) => DataRow(
              cells: [
                DataCell(Text(price.id.toString())),
                DataCell(Text(price.idTipoTransporte.toString())),
                DataCell(Text('\$${price.monto.toStringAsFixed(2)}')),
              ],
            ),
          )
          .toList(),
    );
  }

  Widget _buildTypeTransportTable() {
    if (_types == null || _types!.isEmpty) {
      return Center(child: Text("No hay tipos de transporte registrados."));
    }
    return DataTable(
      columns: const [
        DataColumn(label: Text("ID")),
        DataColumn(label: Text("Tipo de Transporte")),
      ],
      rows: _types!
          .map(
            (type) => DataRow(
              cells: [
                DataCell(Text(type.id.toString())),
                DataCell(Text(type.nombre)),
              ],
            ),
          )
          .toList(),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Precios y Tipos de Transporte'),
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: _loading ? null : _fetchAll,
            tooltip: "Refrescar",
          ),
        ],
      ),
      body: _loading
          ? Center(child: CircularProgressIndicator())
          : _error != null
              ? Center(child: Text(_error!, style: TextStyle(color: Colors.red)))
              : SingleChildScrollView(
                  padding: EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Tabla de Precios', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
                      SizedBox(height: 8),
                      SingleChildScrollView(
                        scrollDirection: Axis.horizontal,
                        child: _buildPricesTable(),
                      ),
                      SizedBox(height: 32),
                      Text('Tabla de Tipos de Transporte', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
                      SizedBox(height: 8),
                      SingleChildScrollView(
                        scrollDirection: Axis.horizontal,
                        child: _buildTypeTransportTable(),
                      ),
                    ],
                  ),
                ),
    );
  }
}

///
///
class Movement {
  final int id;
  final int cardId;
  final String? tipoMovimiento;
  final String? tipoTransporte;
  final double? monto;
  final DateTime? fecha;
  final String? origen;
  final String? destino;
  final String? estado;

  Movement({
    required this.id,
    required this.cardId,
    this.tipoMovimiento,
    this.tipoTransporte,
    this.monto,
    this.fecha,
    this.origen,
    this.destino,
    this.estado,
  });

  factory Movement.fromJson(Map<String, dynamic> json) {
    return Movement(
      id: json['ID'] ?? 0,
      cardId: json['CardID'] ?? json['IDTarjeta'] ?? 0,
      tipoMovimiento: json['TipoMovimiento'],
      tipoTransporte: json['TipoTransporte'],
      monto: json['Monto'] != null 
          ? (json['Monto'] is int ? (json['Monto'] as int).toDouble() : json['Monto'] as double)
          : null,
      fecha: json['Fecha'] != null ? DateTime.tryParse(json['Fecha']) : null,
      origen: json['Origen'],
      destino: json['Destino'],
      estado: json['Estado'],
    );
  }
}

class CardIdInputWidget extends StatefulWidget {
  final String token;
  final Function(int)? onCardSelected;

  const CardIdInputWidget({
    Key? key, 
    required this.token,
    this.onCardSelected,
  }) : super(key: key);

  @override
  State<CardIdInputWidget> createState() => _CardIdInputWidgetState();
}

class _CardIdInputWidgetState extends State<CardIdInputWidget>
    with TickerProviderStateMixin {
  final _controller = TextEditingController();
  final _formKey = GlobalKey<FormState>();
  
  int? _cardId;
  bool _showMovements = false;
  bool _isSearching = false;
  String? _errorMessage;
  
  late AnimationController _animationController;
  late Animation<double> _fadeAnimation;
  late Animation<double> _slideAnimation;

  @override
  void initState() {
    super.initState();
    _setupAnimations();
  }

  void _setupAnimations() {
    _animationController = AnimationController(
      duration: Duration(milliseconds: 600),
      vsync: this,
    );

    _fadeAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _animationController, curve: Curves.easeInOut),
    );

    _slideAnimation = Tween<double>(begin: 30.0, end: 0.0).animate(
      CurvedAnimation(parent: _animationController, curve: Curves.easeOutBack),
    );

    _animationController.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    _animationController.dispose();
    super.dispose();
  }

  void _consultarMovimientos() async {
    if (!_formKey.currentState!.validate()) return;

    final cardId = int.tryParse(_controller.text);
    if (cardId == null) {
      setState(() {
        _errorMessage = "ID de tarjeta inválido";
      });
      return;
    }

    setState(() {
      _isSearching = true;
      _errorMessage = null;
      _showMovements = false;
    });

    // Simulate search delay for better UX
    await Future.delayed(Duration(milliseconds: 500));

    setState(() {
      _cardId = cardId;
      _showMovements = true;
      _isSearching = false;
    });

    widget.onCardSelected?.call(cardId);
  }

  void _clearSearch() {
    setState(() {
      _controller.clear();
      _cardId = null;
      _showMovements = false;
      _errorMessage = null;
    });
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _animationController,
      builder: (context, child) {
        return Transform.translate(
          offset: Offset(0, _slideAnimation.value),
          child: FadeTransition(
            opacity: _fadeAnimation,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Search Card
                Card(
                  elevation: 4,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Padding(
                    padding: EdgeInsets.all(20),
                    child: Form(
                      key: _formKey,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          // Header
                          Row(
                            children: [
                              Container(
                                padding: EdgeInsets.all(12),
                                decoration: BoxDecoration(
                                  color: Theme.of(context).primaryColor.withOpacity(0.1),
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: Icon(
                                  Icons.credit_card,
                                  color: Theme.of(context).primaryColor,
                                  size: 24,
                                ),
                              ),
                              SizedBox(width: 16),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      'Consultar Movimientos',
                                      style: Theme.of(context).textTheme.titleLarge?.copyWith(
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                    Text(
                                      'Ingrese el ID de la tarjeta',
                                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                        color: Colors.grey[600],
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),

                          SizedBox(height: 20),

                          // Card ID Input
                          TextFormField(
                            controller: _controller,
                            keyboardType: TextInputType.number,
                            inputFormatters: [
                              FilteringTextInputFormatter.digitsOnly,
                              LengthLimitingTextInputFormatter(10),
                            ],
                            decoration: InputDecoration(
                              labelText: 'ID de la Tarjeta',
                              hintText: 'Ej: 12345',
                              prefixIcon: Icon(Icons.credit_card),
                              suffixIcon: _controller.text.isNotEmpty
                                  ? IconButton(
                                      icon: Icon(Icons.clear),
                                      onPressed: _clearSearch,
                                    )
                                  : null,
                              border: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(12),
                              ),
                              contentPadding: EdgeInsets.symmetric(
                                horizontal: 16, 
                                vertical: 16,
                              ),
                            ),
                            validator: (value) {
                              if (value == null || value.isEmpty) {
                                return 'Ingrese el ID de la tarjeta';
                              }
                              if (int.tryParse(value) == null) {
                                return 'ID debe ser un número válido';
                              }
                              return null;
                            },
                            onChanged: (value) {
                              setState(() {
                                _errorMessage = null;
                              });
                            },
                            onFieldSubmitted: (value) => _consultarMovimientos(),
                          ),

                          SizedBox(height: 20),

                          // Search Button
                          AnimatedContainer(
                            duration: Duration(milliseconds: 300),
                            height: 56,
                            child: ElevatedButton.icon(
                              onPressed: _isSearching ? null : _consultarMovimientos,
                              icon: _isSearching
                                  ? SizedBox(
                                      width: 20,
                                      height: 20,
                                      child: CircularProgressIndicator(
                                        strokeWidth: 2,
                                        valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                                      ),
                                    )
                                  : Icon(Icons.search),
                              label: Text(
                                _isSearching ? 'Buscando...' : 'Consultar Movimientos',
                                style: TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.w600,
                                ),
                              ),
                              style: ElevatedButton.styleFrom(
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                elevation: _isSearching ? 0 : 4,
                              ),
                            ),
                          ),

                          // Error Message
                          if (_errorMessage != null) ...[
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
                                  Icon(Icons.error, color: Colors.red, size: 20),
                                  SizedBox(width: 8),
                                  Expanded(
                                    child: Text(
                                      _errorMessage!,
                                      style: TextStyle(color: Colors.red[800]),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ],
                      ),
                    ),
                  ),
                ),

                SizedBox(height: 16),

                // Movements Display
                if (_showMovements && _cardId != null)
                  Expanded(
                    child: MovementByCardIdWidget(
                      cardId: _cardId!,
                      token: widget.token,
                    ),
                  ),
              ],
            ),
          ),
        );
      },
    );
  }
}

class MovementByCardIdWidget extends StatefulWidget {
  final int cardId;
  final String token;

  const MovementByCardIdWidget({
    Key? key,
    required this.cardId,
    required this.token,
  }) : super(key: key);

  @override
  State<MovementByCardIdWidget> createState() => _MovementByCardIdWidgetState();
}

class _MovementByCardIdWidgetState extends State<MovementByCardIdWidget>
    with TickerProviderStateMixin {
  late Future<List<Movement>> _futureMovements;
  late AnimationController _listAnimationController;
  
  @override
  void initState() {
    super.initState();
    _listAnimationController = AnimationController(
      duration: Duration(milliseconds: 800),
      vsync: this,
    );
    _futureMovements = fetchMovements();
    _listAnimationController.forward();
  }

  @override
  void didUpdateWidget(MovementByCardIdWidget oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.cardId != widget.cardId) {
      _futureMovements = fetchMovements();
      _listAnimationController.reset();
      _listAnimationController.forward();
    }
  }

  @override
  void dispose() {
    _listAnimationController.dispose();
    super.dispose();
  }

  Future<List<Movement>> fetchMovements() async {
    try {
      final url = Uri.parse(
        '${AppConfig.baseUrl}/movement/pasajero/bycardid?ID=${widget.cardId}',
      );
      
      final response = await http.get(
        url,
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'Content-Type': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data is List) {
          return data.map((json) => Movement.fromJson(json)).toList();
        } else {
          return [];
        }
      } else if (response.statusCode == 404) {
        return [];
      } else {
        throw Exception('Error ${response.statusCode}: ${response.body}');
      }
    } catch (e) {
      throw Exception('Error de conexión: $e');
    }
  }

  void _refreshMovements() {
    setState(() {
      _futureMovements = fetchMovements();
    });
  }

  IconData _getMovementIcon(String? tipoMovimiento) {
    if (tipoMovimiento == null) return Icons.swap_horiz;
    
    final tipo = tipoMovimiento.toLowerCase();
    if (tipo.contains('entrada') || tipo.contains('ingreso')) {
      return Icons.login;
    } else if (tipo.contains('salida') || tipo.contains('egreso')) {
      return Icons.logout;
    } else if (tipo.contains('2')) {
      return Icons.add_circle;
    } else if (tipo.contains('1')) {
      return Icons.payment;
    } else {
      return Icons.swap_horiz;
    }
  }

  Color _getMovementColor(String? tipoMovimiento) {
    if (tipoMovimiento == null) return Colors.grey;
    
    final tipo = tipoMovimiento.toLowerCase();
    if (tipo.contains('entrada') || tipo.contains('ingreso') || tipo.contains('recarga')) {
      return Colors.green;
    } else if (tipo.contains('salida') || tipo.contains('egreso') || tipo.contains('pago')) {
      return Colors.red;
    } else {
      return Colors.blue;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
      ),
      child: Column(
        children: [
          // Header
          Container(
            padding: EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: Theme.of(context).primaryColor.withOpacity(0.1),
              borderRadius: BorderRadius.only(
                topLeft: Radius.circular(16),
                topRight: Radius.circular(16),
              ),
            ),
            child: Row(
              children: [
                Icon(
                  Icons.history,
                  color: Theme.of(context).primaryColor,
                ),
                SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Movimientos de la Tarjeta',
                        style: Theme.of(context).textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      Text(
                        'ID: ${widget.cardId}',
                        style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          color: Colors.grey[600],
                        ),
                      ),
                    ],
                  ),
                ),
                IconButton(
                  onPressed: _refreshMovements,
                  icon: Icon(Icons.refresh),
                  tooltip: 'Actualizar',
                ),
              ],
            ),
          ),

          // Content
          Expanded(
            child: FutureBuilder<List<Movement>>(
              future: _futureMovements,
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return _buildLoadingState();
                } else if (snapshot.hasError) {
                  return _buildErrorState(snapshot.error.toString());
                } else if (snapshot.hasData) {
                  final movements = snapshot.data!;
                  if (movements.isEmpty) {
                    return _buildEmptyState();
                  }
                  return _buildMovementsList(movements);
                } else {
                  return _buildEmptyState();
                }
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLoadingState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          CircularProgressIndicator(
            valueColor: AlwaysStoppedAnimation<Color>(Theme.of(context).primaryColor),
          ),
          SizedBox(height: 16),
          Text(
            'Cargando movimientos...',
            style: Theme.of(context).textTheme.bodyLarge,
          ),
        ],
      ),
    );
  }

  Widget _buildErrorState(String error) {
    return Center(
      child: Padding(
        padding: EdgeInsets.all(20),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.error_outline,
              size: 64,
              color: Colors.red,
            ),
            SizedBox(height: 16),
            Text(
              'Error al cargar movimientos',
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 8),
            Text(
              error,
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.grey[600]),
            ),
            SizedBox(height: 16),
            ElevatedButton.icon(
              onPressed: _refreshMovements,
              icon: Icon(Icons.refresh),
              label: Text('Reintentar'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Padding(
        padding: EdgeInsets.all(20),
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
              'No hay movimientos',
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 8),
            Text(
              'Esta tarjeta no tiene movimientos registrados',
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.grey[600]),
            ),
            SizedBox(height: 16),
            TextButton.icon(
              onPressed: _refreshMovements,
              icon: Icon(Icons.refresh),
              label: Text('Actualizar'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMovementsList(List<Movement> movements) {
    return AnimatedBuilder(
      animation: _listAnimationController,
      builder: (context, child) {
        return ListView.builder(
          padding: EdgeInsets.all(16),
          itemCount: movements.length,
          itemBuilder: (context, index) {
            final movement = movements[index];
            final delay = index * 0.1;
            final animation = Tween<double>(begin: 0.0, end: 1.0).animate(
              CurvedAnimation(
                parent: _listAnimationController,
                curve: Interval(delay, 1.0, curve: Curves.easeOutBack),
              ),
            );

            return FadeTransition(
              opacity: animation,
              child: SlideTransition(
                position: Tween<Offset>(
                  begin: Offset(0.3, 0),
                  end: Offset.zero,
                ).animate(animation),
                child: Container(
                  margin: EdgeInsets.only(bottom: 12),
                  child: Card(
                    elevation: 2,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: ListTile(
                      contentPadding: EdgeInsets.all(16),
                      leading: Container(
                        padding: EdgeInsets.all(8),
                        decoration: BoxDecoration(
                          color: _getMovementColor(movement.tipoMovimiento).withOpacity(0.1),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Icon(
                          _getMovementIcon(movement.tipoMovimiento),
                          color: _getMovementColor(movement.tipoMovimiento),
                        ),
                      ),
                      title: Text(
                        movement.tipoMovimiento ?? 'Movimiento #${movement.id}',
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          if (movement.tipoTransporte != null) ...[
                            SizedBox(height: 4),
                            Row(
                              children: [
                                Icon(Icons.directions, size: 16, color: Colors.grey),
                                SizedBox(width: 4),
                                Text(movement.tipoTransporte!),
                              ],
                            ),
                          ],
                          if (movement.origen != null || movement.destino != null) ...[
                            SizedBox(height: 4),
                            Row(
                              children: [
                                Icon(Icons.location_on, size: 16, color: Colors.grey),
                                SizedBox(width: 4),
                                Expanded(
                                  child: Text(
                                    '${movement.origen ?? "N/A"} → ${movement.destino ?? "N/A"}',
                                    overflow: TextOverflow.ellipsis,
                                  ),
                                ),
                              ],
                            ),
                          ],
                          if (movement.fecha != null) ...[
                            SizedBox(height: 4),
                            Row(
                              children: [
                                Icon(Icons.access_time, size: 16, color: Colors.grey),
                                SizedBox(width: 4),
                                Text(
                                  '${movement.fecha!.day}/${movement.fecha!.month}/${movement.fecha!.year} ${movement.fecha!.hour}:${movement.fecha!.minute.toString().padLeft(2, '0')}',
                                ),
                              ],
                            ),
                          ],
                        ],
                      ),
                      trailing: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        crossAxisAlignment: CrossAxisAlignment.end,
                        children: [
                          if (movement.monto != null)
                            Text(
                              '\$${movement.monto!.toStringAsFixed(2)}',
                              style: TextStyle(
                                fontWeight: FontWeight.bold,
                                color: _getMovementColor(movement.tipoMovimiento),
                                fontSize: 16,
                              ),
                            ),
                          if (movement.estado != null) ...[
                            SizedBox(height: 4),
                            Container(
                              padding: EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                              decoration: BoxDecoration(
                                color: movement.estado == 'Completado' 
                                    ? Colors.green.withOpacity(0.1)
                                    : Colors.orange.withOpacity(0.1),
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: Text(
                                movement.estado!,
                                style: TextStyle(
                                  fontSize: 12,
                                  color: movement.estado == 'Completado' 
                                      ? Colors.green[700]
                                      : Colors.orange[700],
                                ),
                              ),
                            ),
                          ],
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            );
          },
        );
      },
    );
  }
}
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
        Uri.parse('$baseUrl/pqr/pasajero/pqrs'),
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
  
  Future<ApiResponse<List<PqrModel>>> getAllPqrs() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/pqr/pqrs'),
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