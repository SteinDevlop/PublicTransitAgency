import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '/pages/login.dart';
import '/pages/administrador.dart';
import '/pages/operario.dart';
import '/pages/pasajero.dart';
import '/pages/supervisor.dart';
import '/pages/tecnico.dart';
import '../config/config.dart';

void main() {
  runApp(MaterialApp(
    initialRoute: '/home', // Cambia la ruta inicial a HomePage
    routes: {
      '/': (context) => LoginPage(),
      '/home': (context) => HomePage(),
      // Elimina los tokens vacíos de las rutas
    },
  ));
}

class TransitConnectApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    SystemChrome.setSystemUIOverlayStyle(SystemUiOverlayStyle(
      statusBarColor: Colors.blue,
      statusBarIconBrightness: Brightness.light,
    ));

    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Transit Connect',
      theme: ThemeData(
        textTheme: GoogleFonts.poppinsTextTheme(),
        primarySwatch: Colors.blue,
      ),
      home: HomePage(),
    );
  }
}

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.blue[800],
        title: Text('Public Transit Agency',
            style: TextStyle(color: Colors.white)),
        actions: [
          IconButton(
            icon: Icon(Icons.notifications, color: Colors.white),
            onPressed: () {},
          ),
          IconButton(
            icon: Icon(Icons.account_circle, color: Colors.white),
            onPressed: () {},
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              SizedBox(height: 24),
              Container(
                width: double.infinity,
                decoration: BoxDecoration(
                  color: Colors.blue[700],
                  borderRadius: BorderRadius.circular(24),
                ),
                padding: EdgeInsets.symmetric(vertical: 32, horizontal: 24),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(Icons.directions_bus,
                            color: Colors.white, size: 40),
                        SizedBox(width: 12),
                        Text(
                          'PORTAL DEL USUARIO',
                          style: TextStyle(
                            fontSize: 28,
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                    SizedBox(height: 12),
                    Text(
                      'Consulta tu saldo, gestiona tus viajes y mantente informado sobre el transporte público',
                      style: TextStyle(
                        fontSize: 16,
                        color: Colors.white,
                      ),
                    ),
                    SizedBox(height: 20),
                    Center(
                      child: ElevatedButton.icon(
                        icon: Icon(Icons.login, color: Colors.blue[700]),
                        label: Text('Ingresar al Portal',
                            style: TextStyle(color: Colors.blue[700])),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.white,
                          foregroundColor: Colors.blue[700],
                          padding: EdgeInsets.symmetric(
                              horizontal: 24, vertical: 12),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(24),
                          ),
                        ),
                        onPressed: () {
                          Navigator.pushNamed(context, '/');
                        },
                      ),
                    ),
                  ],
                ),
              ),
              SizedBox(height: 24),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Container(
                      margin: EdgeInsets.symmetric(horizontal: 6),
                      padding: EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: Colors.blue[50],
                        borderRadius: BorderRadius.circular(18),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black12,
                            blurRadius: 4,
                            offset: Offset(0, 2),
                          ),
                        ],
                      ),
                      child: Column(
                        children: [
                          Icon(Icons.account_balance_wallet,
                              color: Colors.blue[700], size: 36),
                          SizedBox(height: 12),
                          Text(
                            'Consultar saldo',
                            style: TextStyle(
                                fontWeight: FontWeight.bold, fontSize: 16),
                            textAlign: TextAlign.center,
                          ),
                          SizedBox(height: 6),
                          Text(
                            'Verifica el saldo de tu tarjeta de transporte en tiempo real',
                            style:
                                TextStyle(fontSize: 12, color: Colors.black54),
                            textAlign: TextAlign.center,
                          ),
                          SizedBox(height: 12),
                          ElevatedButton(
                            onPressed: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                    builder: (_) => CardBalanceScreen()),
                              );
                            },
                            child: Text('Consultar'),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.blue[700],
                              foregroundColor: Colors.white,
                              minimumSize: Size(double.infinity, 36),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(12),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  Expanded(
                    child: Container(
                      margin: EdgeInsets.symmetric(horizontal: 6),
                      padding: EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: Colors.green[50],
                        borderRadius: BorderRadius.circular(18),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black12,
                            blurRadius: 4,
                            offset: Offset(0, 2),
                          ),
                        ],
                      ),
                      child: Column(
                        children: [
                          Icon(Icons.map, color: Colors.green[700], size: 36),
                          SizedBox(height: 12),
                          Text(
                            'Rutas',
                            style: TextStyle(
                                fontWeight: FontWeight.bold, fontSize: 16),
                            textAlign: TextAlign.center,
                          ),
                          SizedBox(height: 6),
                          Text(
                            'Consulta las rutas disponibles y los horarios de servicio',
                            style:
                                TextStyle(fontSize: 12, color: Colors.black54),
                            textAlign: TextAlign.center,
                          ),
                          SizedBox(height: 12),
                          ElevatedButton(
                            onPressed: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(builder: (_) => RoutesStopsScreen()),
                              );
                            },
                            child: Text('Ver rutas'),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.green[700],
                              foregroundColor: Colors.white,
                              minimumSize: Size(double.infinity, 36),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(12),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  Expanded(
                    child: Container(
                      margin: EdgeInsets.symmetric(horizontal: 6),
                      padding: EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: Colors.amber[50],
                        borderRadius: BorderRadius.circular(18),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black12,
                            blurRadius: 4,
                            offset: Offset(0, 2),
                          ),
                        ],
                      ),
                      child: Column(
                        children: [
                          Icon(Icons.announcement,
                              color: Colors.amber[800], size: 36),
                          SizedBox(height: 12),
                          Text(
                            'Avisos y noticias',
                            style: TextStyle(
                                fontWeight: FontWeight.bold, fontSize: 16),
                            textAlign: TextAlign.center,
                          ),
                          SizedBox(height: 6),
                          Text(
                            'Mantente informado sobre cambios y noticias importantes',
                            style:
                                TextStyle(fontSize: 12, color: Colors.black54),
                            textAlign: TextAlign.center,
                          ),
                          SizedBox(height: 12),
                          ElevatedButton(
                            onPressed: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(builder: (_) => IncidentsScreen()),
                              );
                            },
                            child: Text('Ver avisos'),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.amber[800],
                              foregroundColor: Colors.white,
                              minimumSize: Size(double.infinity, 36),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(12),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            DrawerHeader(
              decoration: BoxDecoration(color: Colors.blue),
              child: Text(
                'Public Transit Agency',
                style: TextStyle(color: Colors.white, fontSize: 24),
              ),
            ),
            _buildDrawerItem(
                context, Icons.account_balance_wallet, 'Consultar saldo'),
            _buildDrawerItem(
                context, Icons.person, 'Portal de usuario', LoginPage()),
            _buildDrawerItem(context, Icons.announcement, 'Avisos'),
            Divider(),
            _buildDrawerItem(
              context,
              Icons.admin_panel_settings,
              'Administrador',
              AdminPanel(token: ''),
            ),
            _buildDrawerItem(
              context,
              Icons.build,
              'Operario',
              OperarioPanel(token: ''),
            ),
            _buildDrawerItem(
              context,
              Icons.directions_bus,
              'Pasajero',
              PassengerPanel(token: ''),
            ),
            _buildDrawerItem(
              context,
              Icons.supervisor_account,
              'Supervisor',
              SupervisorDashboard(token: ''),
            ),
            _buildDrawerItem(
              context,
              Icons.engineering,
              'Técnico',
              TecnicoPanel(token: ''),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDrawerItem(BuildContext context, IconData icon, String title,
      [Widget? page]) {
    return ListTile(
      leading: Icon(icon),
      title: Text(title),
      onTap: page != null
          ? () => Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => page),
              )
          : null,
    );
  }
}

class CardBalanceScreen extends StatefulWidget {
  @override
  _CardBalanceScreenState createState() => _CardBalanceScreenState();
}

class _CardBalanceScreenState extends State<CardBalanceScreen> {
  final TextEditingController _idController = TextEditingController();
  bool _loading = false;
  String? _error;
  Map<String, dynamic>? _cardData;

  Future<void> _consultarSaldo() async {
    setState(() {
      _loading = true;
      _error = null;
      _cardData = null;
    });
    final id = _idController.text.trim();
    if (id.isEmpty) {
      setState(() {
        _loading = false;
        _error = 'Por favor ingresa el ID de la tarjeta';
      });
      return;
    }
    try {
      final response = await http.get(
        Uri.parse('https://publictransitagency-production.up.railway.app/card/tarjeta?ID=$id'),
        headers: {'accept': 'application/json'},
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          _cardData = data;
        });
      } else {
        setState(() {
          _error = 'No se encontró la tarjeta o error en la consulta';
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
        title: Text('Consultar Saldo de Tarjeta'),
        backgroundColor: Colors.blue[700],
      ),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            TextField(
              controller: _idController,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(
                labelText: 'ID de la tarjeta',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.credit_card),
              ),
            ),
            const SizedBox(height: 20),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _loading ? null : _consultarSaldo,
                child: _loading
                    ? SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(
                            strokeWidth: 2, color: Colors.white),
                      )
                    : Text('Consultar saldo'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.blue[700],
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
            if (_cardData != null) ...[
              const SizedBox(height: 32),
              Card(
                elevation: 4,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      Icon(Icons.credit_card,
                          color: Colors.blue[700], size: 48),
                      const SizedBox(height: 12),
                      Text('ID Tarjeta',
                          style:
                              TextStyle(fontSize: 16, color: Colors.black54)),
                      Text(
                        _cardData!['ID']?.toString() ?? '-',
                        style: TextStyle(
                            fontSize: 28,
                            fontWeight: FontWeight.bold,
                            color: Colors.blue[800]),
                      ),
                      const SizedBox(height: 16),
                      Text('Saldo disponible',
                          style:
                              TextStyle(fontSize: 16, color: Colors.black54)),
                      Text(
                        _cardData!['Saldo']?.toString() ?? '-',
                        style: TextStyle(
                            fontSize: 32,
                            fontWeight: FontWeight.bold,
                            color: Colors.green[700]),
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

// --- NUEVO: Pantalla para ver rutas y paradas ---
class RoutesStopsScreen extends StatefulWidget {
  @override
  _RoutesStopsScreenState createState() => _RoutesStopsScreenState();
}

class _RoutesStopsScreenState extends State<RoutesStopsScreen> {
  bool _loading = false;
  String? _error;
  List<dynamic>? _routes;

  Future<void> _fetchRoutes() async {
    setState(() {
      _loading = true;
      _error = null;
      _routes = null;
    });
    try {
      final response = await http.get(
        Uri.parse('https://publictransitagency-production.up.railway.app/routes/solo_nombres'),
        headers: {'accept': 'application/json'},
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          _routes = data is List ? data : [];
        });
      } else {
        setState(() {
          _error = 'No se pudieron obtener las rutas/paradas';
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
  void initState() {
    super.initState();
    _fetchRoutes();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Rutas y Paradas'),
        backgroundColor: Colors.green[700],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: _loading
            ? Center(child: CircularProgressIndicator())
            : _error != null
                ? Center(child: Text(_error!, style: TextStyle(color: Colors.red)))
                : _routes == null
                    ? SizedBox()
                    : ListView.builder(
                        itemCount: _routes!.length,
                        itemBuilder: (context, index) {
                          final item = _routes![index];
                          return Card(
                            child: ListTile(
                              title: Text(item.toString()),
                            ),
                          );
                        },
                      ),
      ),
    );
  }
}

// --- NUEVO: Pantalla para ver incidencias ---
class IncidentsScreen extends StatefulWidget {
  @override
  _IncidentsScreenState createState() => _IncidentsScreenState();
}

class _IncidentsScreenState extends State<IncidentsScreen> {
  bool _loading = false;
  String? _error;
  List<dynamic>? _incidents;

  Future<void> _fetchIncidents() async {
    setState(() {
      _loading = true;
      _error = null;
      _incidents = null;
    });
    try {
      final response = await http.get(
        Uri.parse('https://publictransitagency-production.up.railway.app/incidences/'),
        headers: {'accept': 'application/json'},
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          _incidents = data is List ? data : [];
        });
      } else {
        setState(() {
          _error = 'No se pudieron obtener las incidencias';
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
  void initState() {
    super.initState();
    _fetchIncidents();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Incidencias'),
        backgroundColor: Colors.amber[800],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: _loading
            ? Center(child: CircularProgressIndicator())
            : _error != null
                ? Center(child: Text(_error!, style: TextStyle(color: Colors.red)))
                : _incidents == null
                    ? SizedBox()
                    : ListView.builder(
                        itemCount: _incidents!.length,
                        itemBuilder: (context, index) {
                          final item = _incidents![index];
                          return Card(
                            elevation: 4,
                            margin: const EdgeInsets.symmetric(vertical: 10, horizontal: 4),
                            color: Colors.amber[50],
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(18),
                              side: BorderSide(
                                color: Colors.amber[800]!,
                                width: 1.2,
                              ),
                            ),
                            child: ListTile(
                              leading: CircleAvatar(
                                backgroundColor: Colors.amber[800],
                                child: Icon(Icons.warning_amber_rounded, color: Colors.white),
                              ),
                              title: Text(
                                item['Descripcion'] ?? 'Sin descripción',
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  color: Colors.amber[900],
                                  fontSize: 17,
                                ),
                              ),
                              subtitle: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  if (item['Tipo'] != null)
                                    Padding(
                                      padding: const EdgeInsets.only(top: 4.0),
                                      child: Text(
                                        'Tipo: ${item['Tipo']}',
                                        style: TextStyle(color: Colors.grey[800]),
                                      ),
                                    ),
                                  if (item['IDUnidad'] != null)
                                    Text(
                                      'Unidad: ${item['IDUnidad']}',
                                      style: TextStyle(color: Colors.grey[700]),
                                    ),
                                  if (item['IDTicket'] != null)
                                    Text(
                                      'Ticket: ${item['IDTicket']}',
                                      style: TextStyle(color: Colors.grey[700]),
                                    ),
                                ],
                              ),
                              trailing: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Icon(Icons.report, color: Colors.amber[800], size: 22),
                                  Text(
                                    '#${item['ID'] ?? '-'}',
                                    style: TextStyle(
                                      color: Colors.amber[800],
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                ],
                              ),
                              isThreeLine: true,
                            ),
                          );
                        },
                      ),
      ),
    );
  }
}
