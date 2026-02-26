export interface VehicleGroup {
    Code: string;
    Name: string;
}

export interface Vehicle {
    Code: string;
    GroupCode: string;
    BranchId: string;
    BranchName: string;
    Name: string;
    SPZ: string;
    BatteryPercentage: number;
    Speed: number;
    Odometer: number;
    LastPosition: {
        Latitude: string;
        Longitude: string;
    };
}

export interface Trip {
    AverageSpeed: number;
    MaxSpeed: number;
    TripType: boolean;
    StartTime: string;
    FinishTime: string;
    TotalDistance: number;
    Purpose?: string;
}

export interface EcoEvent {
    EventType: number;
    EventValue: number;
    Timestamp: string;
    EventSeverity: number;
    Speed: number;
    Position: {
        Latitude: number;
        Longitude: number;
    };
}
