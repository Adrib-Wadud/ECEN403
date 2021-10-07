package com.example.solar_powered_air_cooler;

import androidx.appcompat.app.AppCompatActivity;

import android.bluetooth.BluetoothSocket;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

public class ManualModeActivity extends AppCompatActivity {
    BluetoothSocket btSocket = MainActivity.btSocket;
    public String chargeLevel;
    public Boolean manualModeActivated = false;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_manual_mode);
        chargeLevel = getIntent().getExtras().getString("Charge");
        TextView charge = (TextView)findViewById(R.id.charge_level_manual);
        charge.setText(chargeLevel);
    }

    public void activateManualMode(View v){
        if(btSocket!=null) {

            MainActivity.sendMessageToServer("Activate Manual Mode!");
            String message = MainActivity.recvdMessageFromServer();
            TextView mode_activated = (TextView)findViewById(R.id.textView24);
            mode_activated.setText("Manual mode activated");
            Toast toast = Toast.makeText(this, message, Toast.LENGTH_SHORT);
            toast.show();
            manualModeActivated = true;

            MainActivity.sendMessageToServer("Get current fan speed!");
            String fan_speed = MainActivity.recvdMessageFromServer();
            TextView fan_speed_t = (TextView)findViewById(R.id.fan_speed);
            fan_speed_t.setText(fan_speed);

            MainActivity.sendMessageToServer("Get current humidity intensity!");
            String humid_t = MainActivity.recvdMessageFromServer();
            TextView humidity_intensity = (TextView)findViewById(R.id.humid_intensity);
            humidity_intensity.setText(humid_t);
        }
        else{
            Toast toast = Toast.makeText(this, "Blueotooth connection not established", Toast.LENGTH_SHORT);
            toast.show();
        }
    }

    public void deactivateManualMode(View v){
        if(btSocket!=null) {
            MainActivity.sendMessageToServer("Deactivate Manual Mode!");
            String message = MainActivity.recvdMessageFromServer();
            TextView mode_activated = (TextView)findViewById(R.id.textView24);
            mode_activated.setText("Manual mode not activated");
            Toast toast = Toast.makeText(this, message, Toast.LENGTH_SHORT);
            toast.show();
            manualModeActivated = false;
        }
        else{
            Toast toast = Toast.makeText(this, "Blueotooth connection not established", Toast.LENGTH_SHORT);
            toast.show();
        }
    }

    public void fanSpeedUp(View v){
        if(btSocket!=null) {
            if(manualModeActivated){
                MainActivity.sendMessageToServer("Fan Speed Up!");
                String message = MainActivity.recvdMessageFromServer();
                Toast toast = Toast.makeText(this, message, Toast.LENGTH_SHORT);
                toast.show();

                MainActivity.sendMessageToServer("Get current fan speed!");
                String fan_speed = MainActivity.recvdMessageFromServer();
                TextView fan_speed_t = (TextView)findViewById(R.id.fan_speed);
                fan_speed_t.setText(fan_speed);

            }
            else{
                Toast toast = Toast.makeText(this, "Manual mode not activated", Toast.LENGTH_SHORT);
                toast.show();
            }

        }
        else{
            Toast toast = Toast.makeText(this, "Blueotooth connection not established", Toast.LENGTH_SHORT);
            toast.show();
        }

    }

    public void fanSpeedDown(View v){
        if(btSocket!=null) {
            if(manualModeActivated){
                MainActivity.sendMessageToServer("Fan Speed Down!");
                String message = MainActivity.recvdMessageFromServer();
                Toast toast = Toast.makeText(this, message, Toast.LENGTH_SHORT);
                toast.show();

                MainActivity.sendMessageToServer("Get current fan speed!");
                String fan_speed = MainActivity.recvdMessageFromServer();
                TextView fan_speed_t = (TextView)findViewById(R.id.fan_speed);
                fan_speed_t.setText(fan_speed);

            }
            else{
                Toast toast = Toast.makeText(this, "Manual mode not activated", Toast.LENGTH_SHORT);
                toast.show();
            }

        }
        else{
            Toast toast = Toast.makeText(this, "Blueotooth connection not established", Toast.LENGTH_SHORT);
            toast.show();
        }

    }

    public void humidIntensityUp(View v){
        if(btSocket!=null) {
            if(manualModeActivated){
                MainActivity.sendMessageToServer("Humidifier Intensity Up!");
                String message = MainActivity.recvdMessageFromServer();
                Toast toast = Toast.makeText(this, message, Toast.LENGTH_SHORT);
                toast.show();

                MainActivity.sendMessageToServer("Get current humidity intensity!");
                String fan_speed = MainActivity.recvdMessageFromServer();
                TextView h_t = (TextView)findViewById(R.id.humid_intensity);
                h_t.setText(fan_speed);

            }
            else{
                Toast toast = Toast.makeText(this, "Manual mode not activated", Toast.LENGTH_SHORT);
                toast.show();
            }

        }
        else{
            Toast toast = Toast.makeText(this, "Blueotooth connection not established", Toast.LENGTH_SHORT);
            toast.show();
        }

    }

    public void humidIntensityDown(View v){
        if(btSocket!=null) {
            if(manualModeActivated){
                MainActivity.sendMessageToServer("Humidifier Intensity Down!");
                String message = MainActivity.recvdMessageFromServer();
                Toast toast = Toast.makeText(this, message, Toast.LENGTH_SHORT);
                toast.show();

                MainActivity.sendMessageToServer("Get current humidity intensity!");
                String fan_speed = MainActivity.recvdMessageFromServer();
                TextView h_t = (TextView)findViewById(R.id.humid_intensity);
                h_t.setText(fan_speed);

            }
            else{
                Toast toast = Toast.makeText(this, "Manual mode not activated", Toast.LENGTH_SHORT);
                toast.show();
            }

        }
        else{
            Toast toast = Toast.makeText(this, "Blueotooth connection not established", Toast.LENGTH_SHORT);
            toast.show();
        }

    }

}