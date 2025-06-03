import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter/services.dart';
import '../config/config.dart';

class OperarioPanel extends StatefulWidget {
  final String token;

  const OperarioPanel({Key? key, required this.token}) : super(key: key);

  @override
  State<OperarioPanel> createState() => _OperarioPanelState();
}

class _OperarioPanelState extends State<OperarioPanel> {
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
          'Panel del Operario',
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
                        backgroundColor: secondaryColor,
                        radius: 24,
                        child: const Icon(Icons.person, color: Colors.white),
                      ),
                      const SizedBox(width: 12),
                      const Expanded(
                        child: Text(
                          'Operario',
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
                        icon: Icons.report_problem_outlined,
                        title: 'Reportar Incidencias y fallas',
                        color: primaryColor,
                        isActive: selectedSection == 'report',
                        onTap: () {
                          setState(() {
                            selectedSection = 'report';
                          });
                        },
                      ),
                      _buildMenuItem(
                        icon: Icons.notifications_active_outlined,
                        title: 'Alertas',
                        color: primaryColor,
                        isActive: selectedSection == 'incidences',
                        onTap: () {
                          setState(() {
                            selectedSection = 'incidences';
                          });
                        },
                      ),
                      _buildMenuItem(
                        icon: Icons.check_circle_outline,
                        title: 'Marcar Asistencia',
                        color: primaryColor,
                        isActive: selectedSection == 'asistencia',
                        onTap: () {
                            selectedSection = 'asistencia';
                            Navigator.of(context).push(
                            MaterialPageRoute(
                            builder: (_) => CrearAsistenciaScreen(token: widget.token),
                            ),
                          );
                        },
                      ),
                      _buildMenuItem(
                        icon: Icons.info_outline,
                        title: 'Información General',
                        color: primaryColor,
                        isActive: selectedSection == 'info',
                        onTap: () {
                          setState(() {
                            selectedSection = 'info';
                          });
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
      case 'incidences':
        return FutureBuilder<List<dynamic>>(
          future: fetchIncidences(),
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return _loadingWidget('Cargando alertas...');
            } else if (snapshot.hasError) {
              return _errorWidget('Error al cargar alertas');
            } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
              return _emptyWidget('No hay alertas.');
            }
            final incidences = snapshot.data!;
            return Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Alertas',
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
      case 'report':
        return CrearIncidenciaWidget(token: widget.token);
      case 'info':
      default:
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
            final turno = data['turno']?.toString() ?? 'No disponible';

            return Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Información General',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF202124),
                  ),
                ),
                const SizedBox(height: 24),
                Row(
                  children: [
                    Expanded(
                      child: Card(
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
                              const Text(
                                'Nombre',
                                style: TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.bold,
                                  color: Color(0xFF202124),
                                ),
                              ),
                              const SizedBox(height: 8),
                              Text(
                                user['Nombre']?.toString() ?? 'No disponible',
                                style: const TextStyle(
                                  fontSize: 18,
                                  color: Color(0xFF5F6368),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Card(
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
                              const Text(
                                'Turno',
                                style: TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.bold,
                                  color: Color(0xFF202124),
                                ),
                              ),
                              const SizedBox(height: 8),
                              Text(
                                turno,
                                style: const TextStyle(
                                  fontSize: 18,
                                  color: Color(0xFF5F6368),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ],
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

class CrearIncidenciaWidget extends StatefulWidget {
  final String token;
  final VoidCallback? onCreated;
  const CrearIncidenciaWidget({required this.token, this.onCreated, Key? key}) : super(key: key);

  @override
  State<CrearIncidenciaWidget> createState() => _CrearIncidenciaWidgetState();
}

class _CrearIncidenciaWidgetState extends State<CrearIncidenciaWidget> {
  final _formKey = GlobalKey<FormState>();
  final _ticketController = TextEditingController();
  final _descripcionController = TextEditingController();
  final _tipoController = TextEditingController();
  final _unidadController = TextEditingController();
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
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/incidences/create'),
      headers: {
        'Authorization': 'Bearer ${widget.token}',
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: {
        'IDTicket': _ticketController.text.trim(),
        'Descripcion': _descripcionController.text.trim(),
        'Tipo': _tipoController.text.trim(),
        'IDUnidad': _unidadController.text.trim(),
      },
    );
    setState(() => _loading = false);
    if (response.statusCode == 200) {
      setState(() {
        _success = 'Incidencia reportada exitosamente.';
        _ticketController.clear();
        _descripcionController.clear();
        _tipoController.clear();
        _unidadController.clear();
      });
      if (widget.onCreated != null) widget.onCreated!();
    } else {
      String msg = 'Error al reportar incidencia';
      try {
        final data = json.decode(response.body);
        msg = data['detail']?.toString() ?? msg;
      } catch (_) {}
      setState(() {
        _error = msg;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 24, horizontal: 8),
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(18)),
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                'Reportar Incidencia o Falla',
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 20,
                  color: Theme.of(context).primaryColor,
                ),
              ),
              const SizedBox(height: 18),
              TextFormField(
                controller: _ticketController,
                decoration: InputDecoration(
                  labelText: 'ID Ticket',
                  prefixIcon: Icon(Icons.receipt_long),
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                ),
                keyboardType: TextInputType.number,
                validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID del ticket' : null,
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: _descripcionController,
                decoration: InputDecoration(
                  labelText: 'Descripción',
                  prefixIcon: Icon(Icons.description),
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                ),
                maxLines: 2,
                validator: (v) => v == null || v.isEmpty ? 'Ingrese la descripción' : null,
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: _tipoController,
                decoration: InputDecoration(
                  labelText: 'Tipo',
                  prefixIcon: Icon(Icons.category),
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                ),
                validator: (v) => v == null || v.isEmpty ? 'Ingrese el tipo' : null,
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: _unidadController,
                decoration: InputDecoration(
                  labelText: 'ID Unidad',
                  prefixIcon: Icon(Icons.directions_bus),
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                ),
                validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID de la unidad' : null,
              ),
              const SizedBox(height: 20),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  icon: _loading
                      ? SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                      : Icon(Icons.report),
                  label: Text(_loading ? 'Enviando...' : 'Reportar'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Theme.of(context).primaryColor,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                  onPressed: _loading ? null : _submit,
                ),
              ),
              if (_error != null) ...[
                const SizedBox(height: 12),
                Text(_error!, style: TextStyle(color: Colors.red)),
              ],
              if (_success != null) ...[
                const SizedBox(height: 12),
                Text(_success!, style: TextStyle(color: Colors.green)),
              ],
            ],
          ),
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
                    ? 'Ingrese el ID Usuario'
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
