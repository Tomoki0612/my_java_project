package main.java.tomoki;

import java.awt.GridLayout;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JPasswordField;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;

public class Login extends JFrame {
    private JTextField usernameField;
    private JPasswordField passwordField;
    private JButton loginButton;

    private boolean authenticate(String username, String password) {
        // 注意: これは単なるデモです。実際のアプリケーションでは
        // データベースを使用し、パスワードは暗号化して保存すべきです。
        return username.equals("admin") && password.equals("password");
    }
   
    public Login() {
        setTitle("ログイン");
        setSize(300, 150);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        JPanel panel = new JPanel();
        panel.setLayout(new GridLayout(3, 2));

        panel.add(new JLabel("ユーザー名:"));
        usernameField = new JTextField();
        panel.add(usernameField);

        panel.add(new JLabel("パスワード:"));
        passwordField = new JPasswordField();
        passwordField.addActionListener(e -> performLogin());
        panel.add(passwordField);

        loginButton = new JButton("ログイン");
        loginButton.addActionListener(e -> performLogin());
         panel.add(loginButton);

        add(panel);
    }
    
    //ログイン時の処理
    private void performLogin() {
        String username = usernameField.getText();
        String password = new String(passwordField.getPassword());
        
        if (authenticate(username, password)) {
            JOptionPane.showMessageDialog(Login.this,
                "ログイン成功！\nようこそ、" + username + "さん！",
                "認証成功", JOptionPane.INFORMATION_MESSAGE);
            // ここに成功後の処理を追加（例：メイン画面を開くなど）
        } else {
            JOptionPane.showMessageDialog(Login.this,
                "ユーザー名またはパスワードが間違っています。",
                "認証失敗", JOptionPane.ERROR_MESSAGE);
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                new Login().setVisible(true);
            }
        });
    }
}