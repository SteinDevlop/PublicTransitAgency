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
      Uri.parse('https://publictransitagency-production.up.railway.app/login/dashboard'),
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
      Uri.parse('https://publictransitagency-production.up.railway.app/schedules/'),
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
        Uri.parse('https://publictransitagency-production.up.railway.app/planificador/ubicaciones'),
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

  @override
  void initState() {
    super.initState();
    _fetchTransportOptions();
  }

  Future<void> _fetchTransportOptions() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      debugPrint('[PagoWidget] Solicitando precios...');
      final pricesResp = await http.get(
        Uri.parse('https://publictransitagency-production.up.railway.app/price/pasajero/prices'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json'
        },
      );
      debugPrint(
          '[PagoWidget] Respuesta precios: statusCode=${pricesResp.statusCode}');
      debugPrint('[PagoWidget] Solicitando tipos de transporte...');
      final transportsResp = await http.get(
        Uri.parse('https://publictransitagency-production.up.railway.app/typetransport/typetransports'),
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
        Uri.parse('https://publictransitagency-production.up.railway.app/transport_units/'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json'
        },
      );
      if (resp.statusCode == 200) {
        final decoded = json.decode(resp.body);
        final unidadesList = (decoded is Map && decoded.containsKey('data'))
            ? decoded['data']
            : [];
        final filtradas = unidadesList
            .where((u) =>
                (u['IDTipo'] is int
                    ? u['IDTipo']
                    : int.tryParse(u['IDTipo'].toString())) ==
                tipoId)
            .toList();
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
        Uri.parse('https://publictransitagency-production.up.railway.app/movement/create'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: {
          'ID': idMovimiento,
          'IDTipoMovimiento': '1',
          'Monto': _selectedMonto.toString(),
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
        Uri.parse('https://publictransitagency-production.up.railway.app/payments/create'),
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
        Uri.parse('https://publictransitagency-production.up.railway.app/payments/$idPago'),
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
      ),
    );
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
            onPressed: () => Navigator.of(context).pop(),
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
        Uri.parse('https://publictransitagency-production.up.railway.app/movement/administrador/crear'),
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
      // 3. POST /movement/create
      final movResp = await http.post(
        Uri.parse('https://publictransitagency-production.up.railway.app/movement/create'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: {
          'ID': nuevoId,
          'IDTipoMovimiento': '2',
          'Monto': montoStr,
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
      final idTarjeta = widget.user['IDTarjeta'] is int
          ? widget.user['IDTarjeta']
          : int.tryParse(widget.user['IDTarjeta']?.toString() ?? '0') ?? 0;
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
        Uri.parse('https://publictransitagency-production.up.railway.app/payments/create'),
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
        Uri.parse('https://publictransitagency-production.up.railway.app/payments/$idPago'),
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
      ),
    );
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
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Cerrar'),
            style: ElevatedButton.styleFrom(backgroundColor: secondaryColor),
          ),
        ),
      ],
    );
  }
}
