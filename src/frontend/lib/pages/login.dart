import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../config/config.dart'; // Importa la configuración

class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Inicio de Sesión'),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Card(
            elevation: 5,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(10),
            ),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Bienvenido',
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 8),
                  const Text('Inicia sesión para continuar'),
                  const SizedBox(height: 20),
                  TextField(
                    controller: _usernameController,
                    decoration: const InputDecoration(
                      labelText: 'ID',
                      hintText: 'Ingresa tu ID',
                    ),
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    controller: _passwordController,
                    obscureText: true,
                    maxLength: 12,
                    decoration: const InputDecoration(
                      labelText: 'Contraseña',
                      hintText: 'Ingresa tu contraseña',
                    ),
                  ),
                  const SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: () async {
                      final username = _usernameController.text;
                      final password = _passwordController.text;

                      try {
                        // Realizar la solicitud POST al backend usando la URL base
                        final response = await http.post(
                          Uri.parse('${AppConfig.baseUrl}/login/token'),
                          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                          body: {'username': username, 'password': password},
                        );

                        if (response.statusCode == 200) {
                          // Parsear la respuesta
                          final data = json.decode(response.body);
                          final token = data['access_token'];
                          final scope = data['scope'];

                          // Redirigir a la página correspondiente según el rol
                          if (scope == 'pasajero') {
                            Navigator.pushNamed(context, '/pasajero');
                          } else if (scope == 'operario') {
                            Navigator.pushNamed(context, '/operario');
                          } else if (scope == 'supervisor') {
                            Navigator.pushNamed(context, '/supervisor');
                          } else if (scope == 'administrador') {
                            Navigator.pushNamed(context, '/administrador');
                          } else if (scope == 'mantenimiento') {
                            Navigator.pushNamed(context, '/mantenimiento');
                          } else {
                            throw Exception('Rol desconocido');
                          }
                        } else {
                          // Mostrar un mensaje de error si las credenciales son incorrectas
                          showDialog(
                            context: context,
                            builder: (context) => AlertDialog(
                              title: const Text('Error'),
                              content: Text('Inicio de sesión fallido: ${response.body}'),
                              actions: [
                                TextButton(
                                  onPressed: () => Navigator.pop(context),
                                  child: const Text('Cerrar'),
                                ),
                              ],
                            ),
                          );
                        }
                      } catch (e) {
                        // Manejar errores de red o del servidor
                        showDialog(
                          context: context,
                          builder: (context) => AlertDialog(
                            title: const Text('Error'),
                            content: Text('Ocurrió un error: $e'),
                            actions: [
                              TextButton(
                                onPressed: () => Navigator.pop(context),
                                child: const Text('Cerrar'),
                              ),
                            ],
                          ),
                        );
                      }
                    },
                    style: ElevatedButton.styleFrom(
                      minimumSize: const Size(double.infinity, 40),
                    ),
                    child: const Text('Iniciar sesión'),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}