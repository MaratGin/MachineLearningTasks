//
//  ViewController.swift
//  GeneticAlgML
//
//  Created by Marat Giniyatov on 03.12.2023.
//

import UIKit
import CoreLocation
import MapKit

class ViewController: UIViewController {
    
    var mapView = {
       let map = MKMapView()
        map.overrideUserInterfaceStyle = .light
        return map
    }()
    
    var routeCoordinates : [City] = []
    var coordinates: [CLLocationCoordinate2D] = []

    var routeOverlay : MKOverlay?

    
    let kazan = [0, 720, 810, 1010, 790, 950]
    let kazanGeo = (55.796127, 49.106414)
    
    let moscow = [720, 0, 340, 189, 209, 960]
    let moscowGeo = (55.755864, 37.617698)
    
    let buxalovo = [810, 340, 0 ,380, 163, 1290]
    let buxalovoGeo = (57.945260, 40.531015)
    
    let pukovo = [1010, 189, 380, 0, 330, 1150]
    let pukovoGeo = (56.928818, 35.964448)
    
    let zadi = [790, 209, 163, 330, 0, 1190]
    let zadiGeo = (56.931917, 39.595537)
    
    let popki = [950, 960, 1290, 1150, 1190, 0]
    let popkiGeo = (50.189237, 44.500275)
    
    
    var distancesDictionary = [String:[Int]]()
    
    let populationSize = 12
    let citiesCount = 6
    let EliteSize = 1

    let tournamentSize = 2
    let maxGenerationsCount = 50

    
    var currentBestChromosome: Chromosome?

//    let maxPosition = Float(FIELD_SIZE-10.0)
    
    

    override func viewDidLoad() {
        super.viewDidLoad()
        distancesDictionary["Казань"] = [0, 720, 810, 1010, 790, 950]
        distancesDictionary["Москва"] = [720, 0, 340, 189, 209, 960]
        distancesDictionary["Бухалово"] = [810, 340, 0 ,380, 163, 1290]
        distancesDictionary["Пуково"] = [1010, 189, 380, 0, 330, 1150]
        distancesDictionary["Зады"] = [790, 209, 163, 330, 0, 1190]
        distancesDictionary["Попки"] = [950, 1960, 1290, 1150, 1190, 0]
        
        let citiesPool = [City(name: "Казань", lat: kazanGeo.0, lon: kazanGeo.1),
                         City(name: "Москва", lat: moscowGeo.0, lon: moscowGeo.1),
                         City(name: "Бухалово", lat: buxalovoGeo.0, lon: buxalovoGeo.1),
                         City(name: "Пуково", lat: pukovoGeo.0, lon: pukovoGeo.1),
                         City(name: "Зады", lat: zadiGeo.0, lon: zadiGeo.1),
                         City(name: "Попки", lat: popkiGeo.0, lon: popkiGeo.1)
        ]

        //create initial Population
        var population = [Chromosome]()
        for _ in 1...populationSize {
            let chromosome = Chromosome(initialCities: citiesPool.shuffled())
            population.append(chromosome)
        }
        for _ in 1...maxGenerationsCount {
            population = createNextGeneration(population: population)
            currentBestChromosome = population.first
            for i in population {
                print(i.cities.description, i.summaryDistance)
            }
                print(currentBestChromosome?.summaryDistance)
        }
        mapView.delegate = self
        setMapConstraints()
        view.backgroundColor = .yellow
        if let unwrapped = currentBestChromosome?.cities {
            for i in unwrapped {
                routeCoordinates.append(i)
                coordinates.append(CLLocationCoordinate2D(latitude: i.lat, longitude: i.lon))
            }
        }
//        routeCoordinates.append(CLLocation(latitude: 50.189237, longitude: 44.500275))
//        routeCoordinates.append(CLLocation(latitude: 56.928818, longitude: 35.964448))
        addPins()
        processRoutes(coordinates: coordinates)

        
    }
    
    func calculateFitness(route: [Int], distanceMatrix: [[Int]]) -> Int {
        return zip(route.dropLast(), route).reduce(0) { $0 + distanceMatrix[$1.0][$1.1] } + distanceMatrix[route.last!][route.first!]
    }
    
    func selectParentTournament(_ population:[Chromosome]) -> Chromosome{
        var tournamentPopulation = [Chromosome]()
        for _ in 1...tournamentSize {
            tournamentPopulation.append(population[Int(arc4random_uniform(UInt32(population.count)))])
        }

        let sortedTournamentPopulation = tournamentPopulation.sorted { (ch1, ch2) -> Bool in
            return ch1.summaryDistance < ch2.summaryDistance
        }
        return sortedTournamentPopulation.first!
    }
    
    func saveElite(_ population: [Chromosome]) -> [Chromosome] {
        //sort by fitness
        let sortedPopulation = population.sorted { (ch1, ch2) -> Bool in
            return ch1.summaryDistance < ch2.summaryDistance
        }
        
        return sortedPopulation.dropLast(populationSize-EliteSize)
    }
    
    func createNextGeneration(population: [Chromosome]) -> [Chromosome] {
        var nextGeneration = [Chromosome]()
        
        nextGeneration.append(contentsOf: saveElite(population))
        
        for _ in 1...populationSize-EliteSize {
            
            let chromosome1 = selectParentTournament(population)
            let chromosome2 = selectParentTournament(population)
            
            
            let gene1 = Int.random(in: 0...citiesCount-1)
            let gene2 = Int.random(in: 0...citiesCount-1)
            
            let crossoverStart = min(gene1, gene2)
            let crossoverEnd = max(gene1, gene2)
            
            var tempChromosome = [City]()
            for index in crossoverStart...crossoverEnd {
                tempChromosome.append(chromosome1.cities[index])
            }
            
            var newChromosome = [City]()
            for city in chromosome2.cities {
                if !tempChromosome.contains(city) {
                    newChromosome.append(city)
                }
            }
            
            newChromosome.insert(contentsOf: tempChromosome, at: crossoverStart)
            var offspring = Chromosome(initialCities: newChromosome)
            offspring.mutate()
            nextGeneration.append(offspring)
        }
        
        return nextGeneration
    }
    
    
    func addPins() {
        var annotations: [MKPointAnnotation] = []
        var index = 1
        if routeCoordinates.count != 0 {
            for i in routeCoordinates {
                let pin = MKPointAnnotation()
                pin.title = i.name + " №\(index)"
                pin.subtitle = i.name + " №\(index)"
                pin.coordinate = CLLocationCoordinate2D(
                    latitude: i.lat,
                    longitude: i.lon
                )
                annotations.append(pin)
                index += 1
            }
        }
        mapView.addAnnotations(annotations)
    }
    
    func drawRoute(routeData: [CLLocation]) {
        if routeCoordinates.count == 0 {
            print("🟡 No Coordinates to draw")
            return
        }
        
        let coordinates = routeCoordinates.map { (location) -> CLLocationCoordinate2D in
            let coord = CLLocation(latitude: location.lat, longitude: location.lon)
            return coord.coordinate
        }
        
        DispatchQueue.main.async {
            self.routeOverlay = MKPolyline(coordinates: coordinates, count: coordinates.count)
            self.mapView.addOverlay(self.routeOverlay!, level: .aboveLabels)
            let customEdgePadding: UIEdgeInsets = UIEdgeInsets(top: 50, left: 50, bottom: 50, right: 20)
            self.mapView.setVisibleMapRect(self.routeOverlay!.boundingMapRect, edgePadding: customEdgePadding, animated: false)
        }
    }
    
    func processRoutes(coordinates: [CLLocationCoordinate2D]) {
        
        for i in 0..<(coordinates.count - 1) {
            showRouteOnMap(pickupCoordinate: coordinates[i], destinationCoordinate: coordinates[i+1])
        }
        showRouteOnMap(pickupCoordinate: coordinates[coordinates.count - 1], destinationCoordinate: coordinates[0])
    }
    
    func showRouteOnMap(pickupCoordinate: CLLocationCoordinate2D, destinationCoordinate: CLLocationCoordinate2D) {

        let sourcePlacemark = MKPlacemark(coordinate: pickupCoordinate, addressDictionary: nil)
        let destinationPlacemark = MKPlacemark(coordinate: destinationCoordinate, addressDictionary: nil)

        let sourceMapItem = MKMapItem(placemark: sourcePlacemark)
        let destinationMapItem = MKMapItem(placemark: destinationPlacemark)

        let sourceAnnotation = MKPointAnnotation()

        if let location = sourcePlacemark.location {
            sourceAnnotation.coordinate = location.coordinate
        }

        let destinationAnnotation = MKPointAnnotation()

        if let location = destinationPlacemark.location {
            destinationAnnotation.coordinate = location.coordinate
        }

        self.mapView.showAnnotations([sourceAnnotation,destinationAnnotation], animated: true )

        let directionRequest = MKDirections.Request()
        directionRequest.source = sourceMapItem
        directionRequest.destination = destinationMapItem
        directionRequest.transportType = .automobile

        // Calculate the direction
        let directions = MKDirections(request: directionRequest)

        directions.calculate {
            (response, error) -> Void in

            guard let response = response else {
                if let error = error {
                    print("Error: \(error)")
                }

                return
            }

            let route = response.routes[0]

            self.mapView.addOverlay((route.polyline), level: MKOverlayLevel.aboveRoads)

            let rect = route.polyline.boundingMapRect
            self.mapView.setRegion(MKCoordinateRegion(rect), animated: true)
        }
    }
    
    func setMapConstraints() {
        view.addSubview(mapView)
        mapView.translatesAutoresizingMaskIntoConstraints = false
        mapView.topAnchor.constraint(equalTo: self.view.topAnchor).isActive = true
        mapView.bottomAnchor.constraint(equalTo: self.view.bottomAnchor).isActive = true
        mapView.leadingAnchor.constraint(equalTo: self.view.leadingAnchor).isActive = true
        mapView.trailingAnchor.constraint(equalTo: self.view.trailingAnchor).isActive = true
    }

}



struct City: Equatable {
    var name = String()
    let lat: Double
    let lon: Double
    
    
    func distance(otherCity: City) -> Double {
        let coordinate0 = CLLocation(latitude: lat, longitude: lon)
        let coordinate1 = CLLocation(latitude: otherCity.lat, longitude: otherCity.lon)

        let distance = coordinate0.distance(from: coordinate1) // result is in meters
        return distance
    }
    
    func position() -> CGPoint {
        return CGPoint(x: Double(lat), y: Double(lon))
    }
    
    static func == (lhs: City, rhs: City) -> Bool {
        return
            lhs.lat == rhs.lat &&
            lhs.lon == rhs.lon
    }
}

struct Chromosome {
    var cities: [City]
    var summaryDistance: Double
    
    init(initialCities: [City]) {
        cities = initialCities
        summaryDistance = 0
        summaryDistance = countSummaryDistance()
    }
    
    private func countSummaryDistance() -> Double {
        var distance = 0.0

        for (index, city) in cities.enumerated() {
            if index > 0 {
                distance += Double(city.distance(otherCity: cities[index-1]))
            }
            if index == cities.count-1 {
                distance += Double(city.distance(otherCity: cities[0]))
            }
        }

        return distance
    }
    
    mutating func mutate() {
        let gene1 = Int.random(in: 0...5)
        let gene2 = Int.random(in: 0...5)
        
        cities.swapAt(gene1, gene2)
//        summaryDistance = countSummaryDistance()
    }
}

extension ViewController: MKMapViewDelegate {
    func mapView(_ mapView: MKMapView, rendererFor overlay: MKOverlay) -> MKOverlayRenderer {
        let renderer = MKGradientPolylineRenderer(overlay: overlay)
        renderer.setColors([
            UIColor(red: 0.06, green: 0.32, blue: 0.10, alpha: 0.72)
        ], locations: [])
        renderer.lineCap = .round
        renderer.lineWidth = 3.0
    return renderer
    }
    
    func mapView(_ mapView: MKMapView, viewFor annotation: MKAnnotation) -> MKAnnotationView? {
        if annotation is MKUserLocation {
            return nil
        }
        
        // Используем стандартный идентификатор аннотации
        let identifier = "MyPin"
        var annotationView = mapView.dequeueReusableAnnotationView(withIdentifier: identifier)
        
        if annotationView == nil {
            annotationView = MKPinAnnotationView(annotation: annotation, reuseIdentifier: identifier)
            annotationView!.canShowCallout = true
            
            // Добавляем кнопку в callout
        } else {
            annotationView!.annotation = annotation
        }
        
        return annotationView
    }

//    func mapView(_ mapView: MKMapView, annotationView view: MKAnnotationView, calloutAccessoryControlTapped control: UIControl) {
//        // При нажатии на кнопку в callout
//        if control == view.rightCalloutAccessoryView {
//            if let annotation = view.annotation {
//                // Показываем алерт с названием места
//                let alert = UIAlertController(title: annotation.title as! String, message: nil, preferredStyle: .alert)
//                alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
//                present(alert, animated: true, completion: nil)
//            }
//        }
//    }
}
