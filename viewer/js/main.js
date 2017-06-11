var renderer, scene, camera, stats;

var particles1, particles2, uniforms, grid;

var PARTICLE_SIZE = 20;

var class_index_to_name = ['bus', 'pickup', 'sedan', 'small', 'sports', 'truck', 'van']

init();
animate();

function initGrid(scene) {
  grid = new THREE.GridHelper( 1000, 20 );
  grid.setColors( 0xffffff, 0xffffff );
  scene.add( grid );
}

function initParticlesForTemplate(template_name, offset) {
  return initParticlesForObject(templates[template_name], offset, 1);
}

function initParticlesForCluster(obj_name, offset) {
  return initParticlesForObject(data[obj_name]['vertices'], offset, 5/3);
}

function initParticlesForObject(vertices, offset, multiplier) {

  var positions = new Float32Array( vertices.length * 3 );
  var colors = new Float32Array( vertices.length * 3 );
  var sizes = new Float32Array( vertices.length );

  var vertex;
  var color = new THREE.Color();

  for ( var i = 0, l = vertices.length; i < l; i ++ ) {

    vertex = vertices[ i ];
    positions[i * 3] = vertex.x * multiplier;
    positions[i * 3 + 1] = vertex.z * multiplier;
    positions[i * 3 + 2] = vertex.y * multiplier;

    color.setHSL( offset + 0.1 * ( i / l ), 1.0, 0.5 );
    color.toArray( colors, i * 3 );

    sizes[ i ] = PARTICLE_SIZE * 0.5;

  }

  var geometry = new THREE.BufferGeometry();
  geometry.addAttribute( 'position', new THREE.BufferAttribute( positions, 3 ) );
  geometry.addAttribute( 'customColor', new THREE.BufferAttribute( colors, 3 ) );
  geometry.addAttribute( 'size', new THREE.BufferAttribute( sizes, 1 ) );

  var material = new THREE.ShaderMaterial( {

    uniforms: {
      color:   { value: new THREE.Color( 0xffffff ) },
      texture: { value: new THREE.TextureLoader().load( "textures/sprites/disc.png" ) }
    },
    vertexShader: document.getElementById( 'vertexshader' ).textContent,
    fragmentShader: document.getElementById( 'fragmentshader' ).textContent,

    alphaTest: 0.9

  } );


  var particles = new THREE.Points( geometry, material );
  return particles;
}

function init() {

  container = document.getElementById( 'container' );

  scene = new THREE.Scene();

  camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 1, 10000 );
  camera.position.y = 150;
  camera.position.z = 350;

  initNav();
  initGrid(scene);
  show(document.getElementById('obj0'), Object.keys(data)[0]);

  renderer = new THREE.WebGLRenderer();
  renderer.setPixelRatio( window.devicePixelRatio );
  renderer.setSize( window.innerWidth, window.innerHeight );
  container.appendChild( renderer.domElement );

  controls = new THREE.OrbitControls( camera, renderer.domElement );

  window.addEventListener( 'resize', onWindowResize, false );

}

function initNav() {
    navigation = document.getElementById('navigation');
    var i = 0;
    for (key in data) {
        var li = document.createElement('li');
        var element = document.createElement('a');
        li.appendChild(element);
        element.innerHTML = i + 1;
        element.id = 'obj' + i;
        wrapper = function(key) { return function() { show(this, key); }}
        element.onclick = wrapper(key);
        navigation.appendChild(li);
        i += 1;
    }
}

function clearNav() {
    for (var i = 0; i < Object.keys(data).length; i++) {
        document.getElementById('obj' + i).className = '';
    }
}

function show(button, obj_name) {
    clearNav();
    button.className += "selected";
    var rotation = 0;

    if (particles1 !== undefined) {
        scene.remove(particles1);
        scene.remove(particles2);
        rotation = particles1.rotation.y;
    }

    particles1 = initParticlesForCluster(obj_name, 0.5);
    particles2 = initParticlesForTemplate(
        class_index_to_name[data[obj_name]['label']], 0.01);

    particles1.rotation.y = rotation;
    particles2.rotation.y = rotation;

    scene.add(particles1);
    scene.add(particles2);
}

function onWindowResize() {

  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();

  renderer.setSize( window.innerWidth, window.innerHeight );

}

function animate() {

  requestAnimationFrame( animate );

  render();

}

function render() {

  rate = 0.005
  particles1.rotation.y += rate;
  particles2.rotation.y += rate;
  grid.rotation.y += rate;

  renderer.render( scene, camera );

}
